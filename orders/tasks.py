from .exchange_rate_service import CurrencyCBRRates
from google_sheets_to_db.celery import app
from .models import Order
from .load_spreadsheet import gsheet2df
from pathlib import Path
import sqlalchemy as sa
import pandas as pd
import numpy as np
import environ
import gspread


# Take environment variables from .env file
CUR_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(Path(str(CUR_DIR)) / '.env')

spreadsheet_name = env('SPREADSHEET_NAME')
connection_string = env('CONNECTION_STR')
update_interval = int(env('UPDATE_INTERVAL'))


@app.task
def get_orders():
    """Loads order data from a spreadsheet into DB"""

    try:
        # Get Pandas DataFrame from spreadsheet
        df = gsheet2df(spreadsheet_name, 0)

        # Calculate and update the 'price_rub' column according the actual USD rate
        current_rates = CurrencyCBRRates()
        usd_rate = current_rates.get_rate_by_code('USD')
        df.loc[df['price_usd'].notna(), 'price_rub'] = df['price_usd'] * usd_rate

        # Pass column 'price rub' to <Int64> safely with <NaN> values handling
        df['price_rub'] = np.floor(pd.to_numeric(df['price_rub'], errors='coerce')).astype('Int64')

        # Connect to SQL and save DataFrame to Order table with replace all values
        engine = sa.create_engine(connection_string)
        engine.connect()
        df.to_sql('orders_order', engine, if_exists='replace', index_label='id')
        return f'Successfully loaded data from spreadsheet <{spreadsheet_name}> into DB'

    except gspread.exceptions.SpreadsheetNotFound:
        return f'Spreadsheet <{spreadsheet_name}> not found.'


@app.task
def update_price_rub():
    """Calculates and updates the 'price_rub' field according the actual USD rate"""

    current_rates = CurrencyCBRRates()
    usd_rate = current_rates.get_rate_by_code('USD')

    for order in Order.objects.all():
        if order.price_usd:
            order.price_rub = round(order.price_usd * usd_rate)
        order.save(update_fields=['price_rub'])
    return f'Actual USD rate is {usd_rate}'
