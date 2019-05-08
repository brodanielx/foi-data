import os
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

from constants import (
    DATE_FORMAT,
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
        create_graphs_for_workbook(workbook)
        

def create_graphs_for_workbook(workbook):
    workbook_category = workbook['category']
    workbook_data = workbook['data']

    for sheet in workbook_data:
        create_graphs_for_sheet(sheet, workbook_category)


def create_graphs_for_sheet(sheet, workbook_category):
    sheet_title = sheet['sheet_title']
    sheet_data = sheet['data']

    if sheet_title == 'Total':
        plot_column_line(sheet_data, 'Total', workbook_category)
    else:
        for col in sheet_data.columns:
            if col != 'Total':
                plot_column_line(sheet_data, col, workbook_category)

    if workbook_category != FOI_CLASS_ATTENDANCE_CATEGORY: 
        plot_bar(sheet_data, sheet_title, workbook_category)


def plot_column_line(data, column, workbook_category):
    style.use('ggplot')

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(data.index, data[column])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    plt.title(f'{column} {workbook_category}')
    plt.xlabel('Date')
    plt.ylabel(f'{workbook_category}')

    file_name = f'{column}_{workbook_category}_line.png'
    full_path = get_file_path(workbook_category, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)


def plot_bar(data, sheet_title, workbook_category):
    data = data.drop(columns=['Total'])
    row = data.iloc[-1]
    date = get_date(data)

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)

    style.use('ggplot')
    row.plot(kind='bar', width=.3)
    plt.title(f'{sheet_title} {workbook_category} {date}')
    plt.xticks(rotation=0)

    file_name = f'{sheet_title}_{workbook_category}_bar.png'
    full_path = get_file_path(workbook_category, file_name)

    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    

def get_date(data_frame):
    data_tail = data_frame.tail(1)
    date = data_tail.index.values[0]
    timestamp = pd.to_datetime(str(date))
    date_str = timestamp.strftime(DATE_FORMAT)
    return date_str

def get_file_path(sub_folder, file_name):
    folder_path = get_folder_path(sub_folder)
    return os.path.join(folder_path, file_name)

def get_folder_path(sub_folder):
    cwd = os.getcwd()
    sub_folder_path = os.path.join('graphs', sub_folder)
    return os.path.join(cwd, sub_folder_path)




if __name__ == '__main__':
    create_graphs()