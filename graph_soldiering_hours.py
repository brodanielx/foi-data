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

from soldiering_constants import (
    CORNER_CATEGORY,
    DOOR_TO_DOOR_CATEGORY,
    SOLDIERING_WORKBOOK_NAME_DICTIONARIES
)


from spreadsheet import (
    get_google_workbooks
)


def get_data():
    workbooks = get_google_workbooks(SOLDIERING_WORKBOOK_NAME_DICTIONARIES)

    corner_workbook = filter_workbook_dictionary_by_category(workbooks, CORNER_CATEGORY)
    door_to_door_workbook = filter_workbook_dictionary_by_category(workbooks, DOOR_TO_DOOR_CATEGORY)


def filter_workbook_dictionary_by_category(workbooks, category):
    return [workbook for workbook in workbooks if workbook['category'] == category][0]