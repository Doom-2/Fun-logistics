import pathlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
import numpy as np

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
    d_frame = d_frame.replace(r'^\s*$', np.nan, regex=True)

    return d_frame
