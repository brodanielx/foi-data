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
    COLUMNS_TO_DROP_FOR_HISTOGRAM
)

from data_utils import (
    get_str_date_of_last_row,
    get_list_of_nth_row
)

from fcn_constants import (
    FCN_CATEGORY,
    FCN_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_concatenated_data_frame_of_non_total_sheets_by_category
)

def get_data_and_plot():
    data, date = get_data_and_date()
    plot(data, date)

    

def get_data_and_date():
    data_frame = get_concatenated_data_frame_of_non_total_sheets_by_category(
        FCN_WORKBOOK_NAME_DICTIONARIES,
        FCN_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM
    )

    date = get_str_date_of_last_row(data_frame)

    return get_list_of_nth_row(data_frame, -1), date


def plot(data, date):
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    counts, bins, patches = ax.hist(
        data,
        bins=10,
        rwidth=.9
    )

    ax.set_xticks(bins)

    plt.title(f'FCN Distribution {date}')
    plt.xlabel(f'FCN')
    plt.ylabel(f'FOI Count')

    plt.show()



if __name__ == '__main__':
    get_data_and_plot()

