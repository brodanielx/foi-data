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

from constants import (
    COLUMNS_TO_DROP_FOR_HISTOGRAM,
    TAIL_ROW_COUNT
)

from data_utils import (
    add_goal_column,
    get_index,
    get_goal_column,
    slice_data_frames_by_tail
)

from fcn_constants import (
    FCN_CATEGORY,
    FCN_INDIVIDUAL_GOAL,
    FCN_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_concatenated_data_frame_of_non_total_sheets_by_category
)

'''
Todo:
- loop through list of names, get_series_by_column_title, plot
'''

def plot_individual_lines_by_category(tail_row_count=0):
    data_frame = get_concatenated_data_frame_of_non_total_sheets_by_category(
        FCN_WORKBOOK_NAME_DICTIONARIES,
        FCN_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM
    )

    names = data_frame.columns
    dates = get_index(data_frame)

    add_goal_column(data_frame, FCN_INDIVIDUAL_GOAL)
    goal = get_goal_column(data_frame)

    if tail_row_count:
        data_frame, goal = slice_data_frames_by_tail(
                            data_frame, goal, 
                            tail_row_count)

    print(data_frame.describe())












if __name__ == '__main__':
    plot_individual_lines_by_category(tail_row_count=TAIL_ROW_COUNT)