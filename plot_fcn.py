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

from fcn_constants import (
    FCN_CATEGORY,
    FCN_GOAL,
    FCN_WORKBOOK_NAME_DICTIONARIES,
    X_LABEL
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot():
    workbooks = get_google_workbooks(FCN_WORKBOOK_NAME_DICTIONARIES)

    fcn_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        FCN_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    add_goal_column(fcn_total_sheet_data_frame, FCN_GOAL)
    goal = get_goal_column(fcn_total_sheet_data_frame)

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
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FCN_CATEGORY}', 
        marker='.',
        color='goldenrod'
    )

    ax.plot(
        x, goal, 
        label=f'{GOAL_LABEL}', 
        linestyle='--',
        color='goldenrod'
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m/%-d/%y'))

    ax.set_ylim(bottom=0)

    plt.title(f'{FCN_CATEGORY}')
    plt.xlabel(X_LABEL)
    plt.ylabel(f'{FCN_CATEGORY}')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot()