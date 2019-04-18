from pprint import pprint

from constants import (
    WORKBOOK_NAME_DICTIONARIES
)
from spreadsheet import (
    get_google_workbooks
)

def create_foi_report():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    fcn_str = get_fcn_str(workbooks)
    print(fcn_str)


def get_fcn_str(workbooks):
    fcn_workbook = next((item for item in workbooks if item['category'] == 'FCN'), None)
    fcn_data = fcn_workbook['data']

    values_str = 'FCN\n'

    return get_workbook_values_str(fcn_data, values_str)

def get_workbook_values_str(workbook_data, values_str):
    for sheet in workbook_data:
        sheet_title = sheet['sheet_title']
        if 'Total' not in sheet_title:
            data = sheet['data']
            data_tail = data.tail(1)
            sheet_values_str = get_sheet_values_str(data_tail)
            values_str += sheet_values_str

    return values_str

def get_sheet_values_str(data_frame):
    sheet_values_str = ''
    series = data_frame.iloc[0]

    for col in data_frame.columns:
        if 'Total' not in col:
            value = series[col]
            value_str = f'{col}: {value}\n'
            sheet_values_str += value_str

    return sheet_values_str




if __name__ == '__main__':
    create_foi_report()