# from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from constants import (
    FCN_SPREADSHEET_ID, FCN_SHEET_NAME
)


scope = [
    # 'https://www.googleapis.com/auth/spreadsheets', 
    'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('FCN_Order_Tampa').sheet1

# data = sheet.row_values(54)
data = sheet.get_all_records()
print(type(data))
# pprint(data)

# def get_google_sheet(spreadsheet_id, sheet_name):
#     """ Retrieve sheet data using OAuth credentials and Google Python API. """
#     scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
#     store = file.Storage('credentials.json')
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets('client_secret.json', scopes)
#         credentials = tools.run_flow(flow, store)
#     service = build('sheets', 'v4', http=credentials.authorize(Http()))
#     gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
#     return gsheet




# if __name__ == '__main__':
#     get_google_sheet(FCN_SPREADSHEET_ID, FCN_SHEET_NAME)
