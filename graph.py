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

from constants import (
    DUES_CATEGORY,
    FCN_CATEGORY,
    FOI_CLASS_ATTENDANCE_CATEGORY,
    WORKBOOK_NAME_DICTIONARIES
)

from spreadsheet import (
    get_google_workbooks
)



def create_graphs():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)

    for workbook in workbooks:
        workbook_category = workbook['category']
        workbook_data = workbook['data']

        for sheet in workbook_data:
            sheet_title = sheet['sheet_title']
            sheet_data = sheet['data']

            if sheet_title == 'Total':
                # graph total line
                plot_column(sheet_data, 'Total', workbook_category)


def plot_column(data, column, workbook_category):
    """ Plot DataFrame """
    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(data.index, data[column])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    plt.title(f'{column} {workbook_category}')
    plt.xlabel('Date')
    plt.ylabel(f'{workbook_category}')
    # plt.style.use('seaborn-deep')

    plt.show()
    # plt.savefig(f'{column}_{workbook_category}.png', bbox_inches='tight')



if __name__ == '__main__':
    create_graphs()