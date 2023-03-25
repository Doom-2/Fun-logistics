import time
import environ
import gspread
import sqlalchemy as sa
from management.commands.load_spreadsheet import gsheet2df
from pathlib import Path
import schedule

# Take environment variables from .env file
CUR_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(Path(str(CUR_DIR)) / '.env')

spreadsheet_name = env('SPREADSHEET_NAME')
connection_string = env('CONNECTION_STR')


def get_orders():
    """
    Loads order data from a spreadsheet into DB
    """

    try:
        df = gsheet2df(spreadsheet_name, 0)
        engine = sa.create_engine(connection_string)
        engine.connect()
        df.to_sql('orders_order', engine, if_exists='replace', index_label='id')
        print('Successfully loaded data from spreadsheet')

    except gspread.exceptions.SpreadsheetNotFound:
        print(f'Spreadsheet {spreadsheet_name} not found.')


schedule.every(30).seconds.do(get_orders)

while True:
    schedule.run_pending()
    time.sleep(1)
