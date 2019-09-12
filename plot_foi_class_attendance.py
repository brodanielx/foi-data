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

from foi_class_attendance_constants import (
    FOI_CLASS_ATTENDANCE_CATEGORY,
    FOI_CLASS_ATTENDANCE_WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_google_workbooks
)



def get_data_and_plot(weeks):
    workbooks = get_google_workbooks(FOI_CLASS_ATTENDANCE_WORKBOOK_NAME_DICTIONARIES)

    foi_class_attendance_total_sheet_data_frame = get_data_frame_by_category_and_sheet_title(
        workbooks, 
        FOI_CLASS_ATTENDANCE_CATEGORY,
        TOTAL_SHEET_TITLE
    )

    dates = get_index(foi_class_attendance_total_sheet_data_frame)

    foi_class_attendance_total_column = get_series_by_column_title(
        foi_class_attendance_total_sheet_data_frame,
        TOTAL_COLUMN_TITLE
    )

    plot_foi_class_attendance_line(
        dates,
        foi_class_attendance_total_column
    )



def plot_foi_class_attendance_line(x, y):
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(
        x, y, 
        label=f'{FOI_CLASS_ATTENDANCE_CATEGORY}', 
        marker='.',
        color='navy'
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    ax.set_ylim(bottom=0)

    plt.title(f'{FOI_CLASS_ATTENDANCE_CATEGORY}')
    plt.xlabel('Week')
    plt.ylabel(f'FOI')

    # file_name = f'{column}_{workbook_category}_line.png'
    # full_path = get_file_path(workbook_category, file_name)

    # plt.savefig(full_path, bbox_inches='tight')
    # plt.close(fig)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    get_data_and_plot(20)