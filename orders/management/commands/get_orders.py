import environ
import gspread
from django.core.management import BaseCommand
import sqlalchemy as sa
from .load_spreadsheet import gsheet2df

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
