import pathlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
from pandas import DataFrame
import numpy as np
from .exchange_rate_service import USD_RATE

CUR_DIR = pathlib.Path(__file__).parent.resolve()


def gsheet2df(spreadsheet_name, sheet_num):
    """ Loads Google spreadsheet to Pandas DataFrame"""

    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    # Retrieve the credentials from .json and authorize access to Google spreadsheets
    credentials = sac.from_json_keyfile_name(f'{CUR_DIR}/google_api_credentials.json', scope)
    client = gspread.authorize(credentials)

    # Open a specific spreadsheet, pull all the records as a dictionary
    # and convert it into a DataFrame, renaming the columns to the same ones as in 'Order' model.
    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    d_frame = pd.DataFrame.from_dict(sheet)
    d_frame.rename(
        columns={'№': 'seq_num', 'заказ №': 'order', 'стоимость,$': 'price_usd', 'срок поставки': 'required_date'},
        inplace=True)

    # Add new column 'price_rub' to DataFrame and replace all empty columns to NumPy 'NaN' value
    d_frame = d_frame.assign(price_rub=np.nan)
    d_frame = d_frame.replace(r'^\s*$', np.nan, regex=True)

    return d_frame


def prepare_df(df: DataFrame):
    """Prepares DataFrame to convert into SQL DB"""

    # Convert all <string> items to <NaN>
    df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')

    # Convert <price_usd> column to <int> with <NaN> support if possible
    try:
        df['price_usd'] = df['price_usd'].astype('Int64')
    except TypeError:
        print('Cannot safely cast non-equivalent float64 to int64')

    # Calculate <price_rub> column according actual USD exchange rate
    df.loc[df['price_usd'].notna(), 'price_rub'] = df['price_usd'] * USD_RATE

    # Safely pass <price_rub> column to <Int64> with <NaN> values saved
    df['price_rub'] = np.floor(pd.to_numeric(df['price_rub'], errors='coerce')).astype('Int64')
