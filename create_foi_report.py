from pprint import pprint

from constants import (
    DUES_CATEGORY,
    FCN_CATEGORY,
    FOI_CLASS_ATTENDANCE_CATEGORY,
    WORKBOOK_NAME_DICTIONARIES
)
from spreadsheet import (
    get_google_workbooks
)

def create_foi_report():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    dues_str = get_workbook_values_str(workbooks, DUES_CATEGORY)
    fcn_str = get_workbook_values_str(workbooks, FCN_CATEGORY)
    foi_class_attendance_str = get_workbook_values_str(
        workbooks, FOI_CLASS_ATTENDANCE_CATEGORY
    )

    values_str = f'{dues_str}\n{fcn_str}\n{foi_class_attendance_str}\n'

    print(values_str)


def get_workbook_values_str(workbooks, category):
    workbook = next((item for item in workbooks if item['category'] == category), None)
    
    workbook_data = workbook['data']

    values_str = f'{category}\n'

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

def handle_dues_data(workbook):
    if workbook['category'] == DUES_CATEGORY:
        workbook_data = workbook['data']
        # for sheet in workbook_data:






if __name__ == '__main__':
    create_foi_report()