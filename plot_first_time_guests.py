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
    TOTAL_COLUMN_TITLE,
    TOTAL_SHEET_TITLE
)

from data_utils import (
    get_data_frame_by_category_and_sheet_title,
    get_index,
    get_series_by_column_title,
    filter_workbook_dictionary_by_category,
    get_workbook_data,
    get_sheet_by_title,
    get_sheet_data
)

from first_time_guest_constants import (
    FIRST_TIME_GUESTS_CATEGORY,
    FIRST_TIME_GUESTS_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot():
    workbooks = get_google_workbooks(FIRST_TIME_GUESTS_WORKBOOK_NAME_DICTIONARIES)

    first_time_guests_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        FIRST_TIME_GUESTS_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    dates = get_index(first_time_guests_total_sheet_data_frame)

    first_time_guests_total_column = get_series_by_column_title(
        first_time_guests_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    plot_first_time_guests_line(
        dates,
        first_time_guests_total_column
    )



def plot_first_time_guests_line(x, y):
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FIRST_TIME_GUESTS_CATEGORY}', 
        marker='o',
        color='teal'
    )

    ax.xaxis.set_major_locator(ticker.IndexLocator(7,0))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))

    ax.set_ylim(bottom=0)

    plt.title(f'{FIRST_TIME_GUESTS_CATEGORY}')
    plt.xlabel('Week')
    plt.ylabel(f'{FIRST_TIME_GUESTS_CATEGORY}')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot()