from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from constants.constants import (
    CLIENT_SECRET_FILEPATH, FCN_WORKBOOK_NAME,
    FOI_CLASS_ATTENDANCE_WORKBOOK_NAME, 
    NUMBER_OF_SHEETS_PER_WORKBOOK,
    NUMBER_OF_SQUADS, SCOPE,
    WORKBOOK_NAME_DICTIONARIES
)

from data_utils import (
    concat_list_of_data_frames_horizontally,
    drop_columns,
    get_str_date_of_last_row,
    get_list_of_data_frames_from_sheets,
    get_list_of_nth_row,
    get_non_total_sheets_by_category
)

def get_google_workbooks(workbook_name_dictionaries):
    workbooks = []
    for workbook_name_dict in  workbook_name_dictionaries:
        workbook_title = workbook_name_dict['workbook_title']
        workbook_data = get_google_workbook(workbook_title)
        workbook = {
            'category' : workbook_name_dict['category'],
            'data' : workbook_data
        }

        workbooks.append(workbook)

    return workbooks


def get_google_workbook(workbook_name):

    client = get_gspread_client()

    sheet_dictionaries = []

    for i in range(NUMBER_OF_SHEETS_PER_WORKBOOK):
        sheet = client.open(workbook_name).get_worksheet(i)
        data_list = sheet.get_all_records()
        data = to_data_frame(data_list)
        data = clean_workbook_data(data, workbook_name)
        sheet_title = sheet.title

        sheet_dictionary = {
            'sheet_title' : sheet_title,
            'data' : data
        }

        sheet_dictionaries.append(sheet_dictionary)

    return sheet_dictionaries


def get_gspread_client():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRET_FILEPATH, SCOPE
    )

    return gspread.authorize(credentials)


def to_data_frame(data_list):
    data = pd.DataFrame(data_list)
    data.set_index('Week', inplace=True)
    return clean_data(data)

def clean_workbook_data(data, workbook_title):
    if workbook_title == FOI_CLASS_ATTENDANCE_WORKBOOK_NAME:
        return data.loc[data.index.dayofweek == 0]
    return data

def clean_data(data):
    data = data.replace(r'', 0)
    data.index = pd.to_datetime(data.index)
    return data

def get_concatenated_data_frame_of_non_total_sheets_by_category(
    workbook_name_dictionaries,
    category,
    columns_to_drop
):
    workbooks = get_google_workbooks(workbook_name_dictionaries)
    sheets = get_non_total_sheets_by_category(workbooks, category)

    data_frames = get_list_of_data_frames_from_sheets(sheets)
    data_frame = concat_list_of_data_frames_horizontally(data_frames)
    return drop_columns(data_frame, columns_to_drop)
