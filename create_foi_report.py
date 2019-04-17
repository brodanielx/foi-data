from pprint import pprint

from constants import (
    WORKBOOK_NAME_DICTIONARIES
)
from spreadsheet import (
    get_google_workbooks
)

def create_foi_report():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    fcn_workbook = next((item for item in workbooks if item['category'] == 'FCN'), None)
    fcn_data = fcn_workbook['data']

    for sheet in fcn_data:
        sheet_title = sheet['sheet_title']
        if 'Total' not in sheet_title:
            data = sheet['data']
            data_tail = data.tail(1) # still a dataframe
            pprint(data_tail)
            print(type(data_tail))

    return fcn_data

if __name__ == '__main__':
    # pprint(create_foi_report(), indent=2)
    create_foi_report()