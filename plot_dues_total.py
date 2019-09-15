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

from matplotlib.dates import MONDAY
from matplotlib.dates import DateFormatter, WeekdayLocator

from constants import (
    GOAL_LABEL,
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

from dues_constants import (
    DUES_CATEGORY,
    DUES_WORKBOOK_NAME_DICTIONARIES,
    TOTAL_GOAL
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot(head_row_count=0, tail_row_count=0):
    workbooks = get_google_workbooks(DUES_WORKBOOK_NAME_DICTIONARIES)

    dues_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        DUES_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    add_goal_column(dues_total_sheet_data_frame, TOTAL_GOAL)
    goal = get_goal_column(dues_total_sheet_data_frame)

    if tail_row_count:
        dues_total_sheet_data_frame, goal = slice_data_frames_by_tail(
                                                dues_total_sheet_data_frame,
                                                goal,
                                                tail_row_count
        )

    dates = get_index(dues_total_sheet_data_frame)

    dues_total_column = get_series_by_column_title(
        dues_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    plot_dues_line(
        dates, dues_total_column, goal
    )


def plot_dues_line(x, y, goal):
    color = 'green'
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{DUES_CATEGORY}', 
        marker='.',
        color=color
    )

    ax.plot(
        x, goal, 
        label=f'{GOAL_LABEL}', 
        linestyle='--',
        color=color
    )

    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
    mondays = WeekdayLocator(MONDAY, interval=4)
    weeks_format  = DateFormatter('%-m/%-d/%y')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_major_formatter(weeks_format)

    ax.set_ylim(bottom=0)

    plt.title(f'{DUES_CATEGORY}')
    plt.xlabel('Date')
    plt.ylabel(f'$')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot(tail_row_count=20)