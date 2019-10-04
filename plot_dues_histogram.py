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
    get_str_date_of_last_row,
    get_list_of_nth_row
)

from dues_constants import (
    COLUMNS_TO_DROP_FOR_HISTOGRAM,
    DUES_CATEGORY,
    DUES_WORKBOOK_NAME_DICTIONARIES
)

from graph import (
    get_file_path
)

from spreadsheet import (
    get_concatenated_data_frame_of_non_total_sheets_by_category
)

def get_data_and_plot():
    data, date = get_data_and_date()
    plot(data, date)

    

def get_data_and_date():
    data_frame = get_concatenated_data_frame_of_non_total_sheets_by_category(
        DUES_WORKBOOK_NAME_DICTIONARIES,
        DUES_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM
    )

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

    plt.title(f'{DUES_CATEGORY} Distribution {date}')
    plt.xlabel(f'{DUES_CATEGORY} ($)')
    plt.ylabel(f'FOI Count')

    file_name = f'{DUES_CATEGORY}_histogram.png'
    full_path = get_file_path(DUES_CATEGORY, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)

    # plt.show()



if __name__ == '__main__':
    get_data_and_plot()

