import gspread as gs
import pandas as pd
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gc = gs.authorize(creds)

SHEET_ID = '1D1ing_OqL0sCNPK2rXL-OheX-bGImPAnHmivfhxuhlU'
SHEET_NAME = 'e-commerce'

df = pd.read_csv('history.csv')
d2g.upload(df, SHEET_ID, SHEET_NAME, credentials=creds, row_names=True)

