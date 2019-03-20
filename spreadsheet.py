import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


scope = [
    # 'https://www.googleapis.com/auth/spreadsheets', 
    'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('FCN_Order_Tampa').sheet1

data = sheet.row_values(57)
pprint(data)