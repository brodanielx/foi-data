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
        FCN_WORKBOOK_NAME_DICTIONARIES,
        FCN_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM
    )

    date = get_str_date_of_last_row(data_frame)

    data = data_frame.tail(1)

    return data, date


def plot(data, date):
    style.use('ggplot')

    # fig = plt.figure(figsize=(15,8))
    # ax = fig.add_subplot(111)
    ax = data.plot(kind='barh', figsize=(15, 8), legend=True, fontsize=12)

    plt.title(f'{FCN_CATEGORY} {date}')
    plt.xlabel(f'{FCN_CATEGORY}')
    plt.ylabel(f'FOI Count')

    file_name = f'{FCN_CATEGORY}_bar.png'
    full_path = get_file_path(FCN_CATEGORY, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close()



if __name__ == '__main__':
    get_data_and_plot()

