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
    filter_workbook_dictionary_by_category,
    get_workbook_data,
    get_sheet_by_title,
    get_sheet_data,
    slice_data_frames_by_tail
)

from foi_class_attendance_constants import (
    FOI_CLASS_ATTENDANCE_CATEGORY,
    FOI_CLASS_ATTENDANCE_GOAL,
    FOI_CLASS_ATTENDANCE_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot(head_row_count=0, tail_row_count=0):
    workbooks = get_google_workbooks(FOI_CLASS_ATTENDANCE_WORKBOOK_NAME_DICTIONARIES)

    foi_class_attendance_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        FOI_CLASS_ATTENDANCE_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    add_goal_column(foi_class_attendance_total_sheet_data_frame, FOI_CLASS_ATTENDANCE_GOAL)
    goal = get_goal_column(foi_class_attendance_total_sheet_data_frame)

    if tail_row_count:
        foi_class_attendance_total_sheet_data_frame, goal = slice_data_frames_by_tail(
                                                        foi_class_attendance_total_sheet_data_frame,
                                                        goal,
                                                        tail_row_count
        )

    dates = get_index(foi_class_attendance_total_sheet_data_frame)

    foi_class_attendance_total_column = get_series_by_column_title(
        foi_class_attendance_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    plot_foi_class_attendance_line(
        dates,
        foi_class_attendance_total_column,
        goal
    )



def plot_foi_class_attendance_line(x, y, goal):
    color = 'navy'
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FOI_CLASS_ATTENDANCE_CATEGORY}', 
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

    plt.title(f'{FOI_CLASS_ATTENDANCE_CATEGORY}')
    plt.xlabel('Date')
    plt.ylabel(f'FOI')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot(tail_row_count=20)