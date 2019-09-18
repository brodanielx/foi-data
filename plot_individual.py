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

from matplotlib.dates import SUNDAY
from matplotlib.dates import DateFormatter, WeekdayLocator

from constants import (
    COLUMNS_TO_DROP_FOR_HISTOGRAM,
    GOAL_LABEL,
    TAIL_ROW_COUNT
)

from data_utils import (
    add_goal_column,
    get_index,
    get_goal_column,
    slice_data_frames_by_tail
)

from fcn_constants import (
    FCN_CATEGORY,
    FCN_INDIVIDUAL_GOAL,
    FCN_WORKBOOK_NAME_DICTIONARIES,
    X_LABEL
)

from graph import (
    get_file_path
)

from spreadsheet import (
    get_concatenated_data_frame_of_non_total_sheets_by_category
)

def plot_individual_lines_by_category(
    workbook_name_dictionaries,
    category,
    columns_to_drop,
    tail_row_count=0
):
    data_frame = get_concatenated_data_frame_of_non_total_sheets_by_category(
        workbook_name_dictionaries,
        category,
        columns_to_drop,
    )

    add_goal_column(data_frame, FCN_INDIVIDUAL_GOAL)
    goal = get_goal_column(data_frame)

    if tail_row_count:
        data_frame, goal = slice_data_frames_by_tail(
                            data_frame, goal, 
                            tail_row_count)

    plot_all_columns(data_frame, goal)



def plot_all_columns(data_frame, goal):
    dates = get_index(data_frame)

    columns = [col for col in data_frame.columns if col != 'Goal']

    for col in columns:
        column_series = data_frame[col]
        plot_fcn_line(dates, column_series, goal)




def plot_fcn_line(x, y, goal):
    color = 'goldenrod'
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FCN_CATEGORY}', 
        marker='.',
        color=color
    )

    ax.plot(
        x, goal, 
        label=f'{GOAL_LABEL}', 
        linestyle='--',
        color=color
    )

    sundays = WeekdayLocator(SUNDAY, interval=4)
    weeks_format  = DateFormatter('%-m/%-d/%y')
    ax.xaxis.set_major_locator(sundays)
    ax.xaxis.set_major_formatter(weeks_format)

    ax.set_ylim(bottom=0)

    plt.title(f'Bro {y.name} {FCN_CATEGORY}')
    plt.xlabel(X_LABEL)
    plt.ylabel(f'{FCN_CATEGORY}')

    file_name = f'{y.name}_{FCN_CATEGORY}_line.png'
    full_path = get_file_path(FCN_CATEGORY, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    # plt.legend()
    # plt.show()




if __name__ == '__main__':
    plot_individual_lines_by_category(
        FCN_WORKBOOK_NAME_DICTIONARIES,
        FCN_CATEGORY,
        COLUMNS_TO_DROP_FOR_HISTOGRAM,
        tail_row_count=TAIL_ROW_COUNT
    )