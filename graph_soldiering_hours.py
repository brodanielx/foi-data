import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.style as style

from constants import (
    TOTAL_SHEET_TITLE
)

from soldiering_constants import (
    HOURS_SOLDIERED_CORNER_CATEGORY,
    HOURS_SOLDIERED_DOOR_TO_DOOR_CATEGORY,
    SOLDIERING_WORKBOOK_NAME_DICTIONARIES
)


from spreadsheet import (
    get_google_workbooks
)


def get_data():
    workbooks = get_google_workbooks(SOLDIERING_WORKBOOK_NAME_DICTIONARIES)

    hours_soldiered_corner_workbook = filter_workbook_dictionary_by_category(
        workbooks, HOURS_SOLDIERED_CORNER_CATEGORY)

    hours_soldiered_door_to_door_workbook = filter_workbook_dictionary_by_category(
        workbooks, HOURS_SOLDIERED_DOOR_TO_DOOR_CATEGORY)

    hours_soldiered_corner_workbook_data = get_workbook_data(
        hours_soldiered_corner_workbook)

    hours_soldiered_door_to_door_workbook_data = get_workbook_data(
        hours_soldiered_door_to_door_workbook)

    hours_soldiered_corner_total_sheet = get_sheet_by_title(
        hours_soldiered_corner_workbook_data, TOTAL_SHEET_TITLE)

    hours_soldiered_door_to_door_total_sheet = get_sheet_by_title(
        hours_soldiered_door_to_door_workbook_data, TOTAL_SHEET_TITLE)

    hours_soldiered_corner_total_sheet_data_frame = get_sheet_data(
        hours_soldiered_corner_total_sheet)

    hours_soldiered_door_to_door_total_sheet_data_frame = get_sheet_data(
        hours_soldiered_door_to_door_total_sheet)

    print(hours_soldiered_corner_total_sheet_data_frame.head())
    print(hours_soldiered_door_to_door_total_sheet_data_frame.head())


def filter_workbook_dictionary_by_category(workbooks, category):
    return [workbook for workbook in workbooks if workbook['category'] == category][0]

def get_workbook_data(workbook):
    return workbook['data']

def get_sheet_by_title(workbook_data, sheet_title):
    return [sheet for sheet in workbook_data if sheet['sheet_title'] == sheet_title][0]

def get_sheet_data(sheet):
    return sheet['data']



if __name__ == '__main__':
    get_data()