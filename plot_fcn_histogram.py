import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.style as style

from data_utils import (
    add_goal_column,
    get_data_frame_by_category_and_sheet_title,
    get_non_total_sheets_by_category,
    slice_data_frames_by_tail
)

from fcn_constants import (
    FCN_CATEGORY,
    FCN_GOAL,
    FCN_WORKBOOK_NAME_DICTIONARIES,
    X_LABEL
)

from spreadsheet import (
    get_google_workbooks
)

'''
Todo:
- Get last row of data
    - loop through non total sheets and make dataframe of all FOI
- plot histogram
'''

def get_data_and_plot():
    workbooks = get_google_workbooks(FCN_WORKBOOK_NAME_DICTIONARIES)

    sheets = get_non_total_sheets_by_category(workbooks, FCN_CATEGORY)

    print(sheets)





if __name__ == '__main__':
    get_data_and_plot()

