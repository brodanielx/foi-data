import numpy as np
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
    concat_list_of_data_frames_horizontally,
    drop_columns,
    get_str_date_of_last_row,
    get_list_of_data_frames_from_sheets,
    get_list_of_nth_row,
    get_non_total_sheets_by_category
)

from dues_constants import (
    COLUMNS_TO_DROP_FOR_HISTOGRAM,
    DUES_CATEGORY,
    DUES_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_google_workbooks
)

def get_data_and_plot():
    data, date = get_data_and_date()
    plot(data, date)

    

def get_data_and_date():
    workbooks = get_google_workbooks(DUES_WORKBOOK_NAME_DICTIONARIES)
    sheets = get_non_total_sheets_by_category(workbooks, DUES_CATEGORY)

    data_frames = get_list_of_data_frames_from_sheets(sheets)
    data_frame = concat_list_of_data_frames_horizontally(data_frames)
    data_frame = drop_columns(data_frame, COLUMNS_TO_DROP_FOR_HISTOGRAM)

    date = get_str_date_of_last_row(data_frame)

    return get_list_of_nth_row(data_frame, -1), date


def plot(data, date):
    color = 'green'
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    counts, bins, patches = ax.hist(
        data,
        bins=10,
        rwidth=.9,
        color=color
    )

    max_count = max(counts)
    ax.set_xticks(bins)
    ax.set_yticks(np.arange(0, max_count+1, 4))

    plt.title(f'FOI Dues Distribution {date}')
    plt.xlabel(f'$')
    plt.ylabel(f'FOI Count')

    plt.show()



if __name__ == '__main__':
    get_data_and_plot()

