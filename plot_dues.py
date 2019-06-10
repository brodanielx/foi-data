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
import matplotlib.ticker as ticker

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
    get_sheet_data
)

from dues_constants import (
    DUES_CATEGORY,
    DUES_WORKBOOK_NAME_DICTIONARIES,
    LOCAL_COLUMN_TITLE,
    REGIONAL_COLUMN_TITLE,
    NATIONAL_COLUMN_TITLE,
    NATIONAL_SECURITY_GOAL,
    NATIONAL_SECURITY_GOAL_LABEL
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot():
    workbooks = get_google_workbooks(DUES_WORKBOOK_NAME_DICTIONARIES)

    dues_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        DUES_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    add_goal_column(dues_total_sheet_data_frame, NATIONAL_SECURITY_GOAL)
    national_security_goal = get_goal_column(dues_total_sheet_data_frame)

    dates = get_index(dues_total_sheet_data_frame)

    dues_total_column = get_series_by_column_title(
        dues_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    dues_national_column = get_series_by_column_title(
        dues_total_sheet_data_frame,
        NATIONAL_COLUMN_TITLE
    )

    dues_regional_column = get_series_by_column_title(
        dues_total_sheet_data_frame,
        REGIONAL_COLUMN_TITLE
    )

    dues_local_column = get_series_by_column_title(
        dues_total_sheet_data_frame,
        LOCAL_COLUMN_TITLE
    )

    plot_fcn_line(
        dates, dues_total_column,
        dues_national_column,
        dues_regional_column,
        dues_local_column,
        national_security_goal
    )


def plot_fcn_line(
    dates, total, national, 
    regional, local, national_security_goal
    ):
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        dates, total, 
        label=f'{TOTAL_COLUMN_TITLE}', 
        marker='.',
        color='black'
    )

    ax.plot(
        dates, national, 
        label=f'{NATIONAL_COLUMN_TITLE}', 
        marker='.',
        color='red'
    )

    ax.plot(
        dates, national_security_goal, 
        label=f'{NATIONAL_SECURITY_GOAL_LABEL}', 
        linestyle='--',
        color='red'
    )

    ax.plot(
        dates, regional, 
        label=f'{REGIONAL_COLUMN_TITLE}', 
        marker='.',
        color='yellow'
    )

    ax.plot(
        dates, local, 
        label=f'{LOCAL_COLUMN_TITLE}', 
        marker='.',
        color='green'
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    ax.set_ylim(bottom=0)

    plt.title(f'{DUES_CATEGORY}')
    plt.xlabel('Week')
    plt.ylabel(f'{DUES_CATEGORY}')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot()