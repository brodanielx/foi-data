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

from constants.constants import (
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

columns_to_drop = [
    '12186 - Chad Muhammad',
    '138078 - Jacobi X',
    '1581 - Theodore Muhammad',
    '203944 - Malik X',
    '211835 - Jordan X',
    '212428 - McKinley X',
    '29220 - Alton Muhammad',
    '32126 - Shakir Muhammad'
]

def get_data_and_plot():
    df, date = get_data_and_date()
    df.rename(columns = lambda col: col.split('- ')[1], inplace=True)

    ds = df.squeeze()
    ds.sort_values(ascending=True, inplace=True)

    foi = list(ds.keys())
    fcn = ds.to_list()

    plot(foi, fcn, date)

    

def get_data_and_date():
    data_frame = get_concatenated_data_frame_of_non_total_sheets_by_category(
        FCN_WORKBOOK_NAME_DICTIONARIES,
        FCN_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM
    )

    date = get_str_date_of_last_row(data_frame)

    data = data_frame.tail(1)
    data.drop(columns=columns_to_drop, inplace=True)

    return data, date


def plot(x_vals, y_vals, date):
    style.use('ggplot')

    x_pos = np.arange(len(x_vals))

    fig = plt.figure(figsize=(10,8))
    # ax = fig.add_subplot(111)
    # ax = data.plot(kind='barh', figsize=(15, 8), legend=True, fontsize=12)

    plt.barh(x_pos, y_vals)

    plt.axvline(x=100, linestyle='--')

    plt.text(100.5, 8,'Goal', color='red')

    for i, val in enumerate(y_vals):
        color = 'white'

        if (val > 99):
            x = val - 7
        elif (val > 5 and val < 100):
            x = val - 5
        elif (val < 6):
            x = 5
            color = 'red'

        plt.text(x, i, str(val), color=color, fontweight='bold', va='center')

    plt.yticks(x_pos, x_vals)

    plt.tight_layout(pad=2.3)

    plt.title(f'Tampa FCN {date}')
    plt.xlabel(f'{FCN_CATEGORY}')
    plt.ylabel(f'FOI')

    file_name = f'{FCN_CATEGORY}_bar.png'
    full_path = get_file_path(FCN_CATEGORY, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close()

    # plt.show()



if __name__ == '__main__':
    get_data_and_plot()

