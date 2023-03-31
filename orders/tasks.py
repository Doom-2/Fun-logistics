from .exchange_rate_service import CurrencyCBRRates
from google_sheets_to_db.celery import app
from .models import Order
from .spreadsheet_service import gsheet2df, prepare_df
from pathlib import Path
import sqlalchemy as sa
import environ
import gspread


# Take environment variables from .env file
CUR_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(Path(str(CUR_DIR)) / '.env')

spreadsheet_name = env('SPREADSHEET_NAME')
connection_string = env('CONNECTION_STR')


@app.task
def get_orders():
    """Loads order data from a spreadsheet into DB"""

    try:
        # Get Pandas DataFrame from a specific spreadsheet
        df = gsheet2df(spreadsheet_name, 0)

        prepare_df(df)

        # Connect to SQL and save DataFrame to <Order> table with replacement of all values
        engine = sa.create_engine(connection_string)
        engine.connect()
        df.to_sql('orders_order', engine, if_exists='replace', index_label='id')
        return f'Successfully loaded data from spreadsheet <{spreadsheet_name}> into DB'

    except gspread.exceptions.SpreadsheetNotFound:
        return f'Spreadsheet <{spreadsheet_name}> not found.'


@app.task
def update_price_rub():
    """Calculates and updates the 'price_rub' field according the actual USD exchange rate"""

    current_rates = CurrencyCBRRates()
    usd_rate = current_rates.get_rate_by_code('USD')

    for order in Order.objects.all():
        if order.price_usd:
            order.price_rub = round(order.price_usd * usd_rate)
        order.save(update_fields=['price_rub'])
    return f'Actual USD rate is {usd_rate}'
