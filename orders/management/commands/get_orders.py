import environ
import gspread
from django.core.management import BaseCommand
import sqlalchemy as sa
from orders.load_spreadsheet import gsheet2df
from orders.exchange_rate_service import CurrencyCBRRates
import pandas as pd
import numpy as np

env = environ.Env()


class Command(BaseCommand):
    help = "Loads order data from a spreadsheet into DB. Format 'python3 manage.py get_orders <spreadsheet_name>'"

    def __init__(self):
        super().__init__()
        self.spreadsheet_name = ''

    def add_arguments(self, parser):
        parser.add_argument('spreadsheet_name', type=str, help='Indicates the name of spreadsheet to be opened')

    def handle(self,  *args, **kwargs) -> None:
        try:
            self.spreadsheet_name = kwargs['spreadsheet_name']

            # Get Pandas DataFrame from spreadsheet
            df = gsheet2df(self.spreadsheet_name, 0)

            # Calculate and update the 'price_rub' column according the actual USD rate
            current_rates = CurrencyCBRRates()
            usd_rate = current_rates.get_rate_by_code('USD')
            df.loc[df['price_usd'].notna(), 'price_rub'] = df['price_usd'] * usd_rate

            # Pass column 'price rub' to <Int64> safely with <NaN> values handling
            df['price_rub'] = np.floor(pd.to_numeric(df['price_rub'], errors='coerce')).astype('Int64')

            # Connect to SQL and save DataFrame to Order table with replace all values
            connection_string = env('CONNECTION_STR')
            engine = sa.create_engine(connection_string)
            engine.connect()
            df.to_sql('orders_order', engine, if_exists='replace', index_label='id')

            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded data from spreadsheet {self.spreadsheet_name} to DB'))
            return
        except gspread.exceptions.SpreadsheetNotFound:
            self.stdout.write(self.style.ERROR(f'Spreadsheet {self.spreadsheet_name} not found.'))
            return
