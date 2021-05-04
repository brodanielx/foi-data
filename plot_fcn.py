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
import matplotlib.ticker as ticker

from matplotlib.dates import SUNDAY
from matplotlib.dates import DateFormatter, WeekdayLocator

from constants.constants import (
    GOAL_LABEL,
    BAY_AREA_COLUMN_TITLE,
    TOTAL_COLUMN_TITLE,
    TOTAL_SHEET_TITLE
)

from data_utils import (
    add_goal_column,
    get_data_frame_by_category_and_sheet_title,
    get_goal_column,
    get_index,
    get_series_by_column_title,
    slice_data_frames_by_tail
)

from fcn_constants import (
    FCN_CATEGORY,
    FCN_GOAL,
    FCN_WORKBOOK_NAME_DICTIONARIES,
    X_LABEL
)

from graph import (
    get_file_path
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot(head_row_count=0, tail_row_count=0):
    workbooks = get_google_workbooks(FCN_WORKBOOK_NAME_DICTIONARIES)

    fcn_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        FCN_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    add_goal_column(fcn_total_sheet_data_frame, FCN_GOAL)
    goal = get_goal_column(fcn_total_sheet_data_frame)

    if tail_row_count:
        fcn_total_sheet_data_frame, goal = slice_data_frames_by_tail(
                                            fcn_total_sheet_data_frame, goal, 
                                            tail_row_count)

    dates = get_index(fcn_total_sheet_data_frame)

    fcn_total_column = get_series_by_column_title(
        fcn_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    plot_fcn_line(
        dates,
        fcn_total_column,
        goal
    )


def plot_fcn_line(x, y, goal):
    color = 'goldenrod'
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FCN_CATEGORY}', 
        marker='.',
        color=color
    )

    ax.plot(
        x, goal, 
        label=f'{GOAL_LABEL}', 
        linestyle='--',
        color=color
    )

    sundays = WeekdayLocator(SUNDAY, interval=4)
    weeks_format  = DateFormatter('%-m/%-d/%y')
    ax.xaxis.set_major_locator(sundays)
    ax.xaxis.set_major_formatter(weeks_format)

    ax.set_ylim(bottom=0)

    plt.title(f'Tampa {FCN_CATEGORY}')
    plt.xlabel(X_LABEL)
    plt.ylabel(f'{FCN_CATEGORY}')

    plt.legend()

    file_name = f'{FCN_CATEGORY}_line.png'
    full_path = get_file_path(FCN_CATEGORY, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    



if __name__ == '__main__':
    get_data_and_plot(tail_row_count=20)