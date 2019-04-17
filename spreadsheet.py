from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from constants import (
    CLIENT_SECRET_FILENAME, FCN_WORKBOOK_NAME, NUMBER_OF_SHEETS_PER_WORKBOOK,
    NUMBER_OF_SQUADS, SCOPE,
    WORKBOOK_NAME_DICTIONARIES
)

def get_google_workbooks(workbook_name_dictionaries):
    workbooks = []
    for workbook_name_dict in  workbook_name_dictionaries:
        workbook_title = workbook_name_dict['workbook_title']
        workbook_data = get_google_workbook(workbook_title)
        workbook = {
            'category' : workbook_name_dict['category'],
            'data' : workbook_data
        }

        workbooks.append(workbook)

    return workbooks


def get_google_workbook(workbook_name):

    client = get_gspread_client()

    sheet_dictionaries = []

    for i in range(NUMBER_OF_SHEETS_PER_WORKBOOK):
        sheet = client.open(workbook_name).get_worksheet(i)
        data_list = sheet.get_all_records()
        data = to_data_frame(data_list)
        sheet_title = sheet.title

        sheet_dictionary = {
            'sheet_title' : sheet_title,
            'data' : data
        }

        sheet_dictionaries.append(sheet_dictionary)

    return sheet_dictionaries


def get_gspread_client():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRET_FILENAME, SCOPE
    )

    return gspread.authorize(credentials)


def to_data_frame(data_list):
    data = pd.DataFrame(data_list)
    data.set_index('Week', inplace=True)
    return clean_data(data)



def get_google_sheet(workbook_name):
    """ 
    Returns all records of first sheet of workbook in the form of a 
    list of dictionaries 
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRET_FILENAME, SCOPE
        )
    client = gspread.authorize(credentials)

    # sheet = client.open(workbook_name).sheet1
    sheet = client.open(workbook_name).get_worksheet(2)
    data = sheet.get_all_records()
    sheet_title = sheet.title
    print(sheet_title)

    return data


def get_data_frame_from_google_sheet(workbook_name):
    data_list = get_google_sheet(workbook_name)
    data = pd.DataFrame(data_list)
    data.set_index('Week', inplace=True)
    return clean_data(data)

def clean_data(data):
    data = data.replace(r'', 0)
    data.index = pd.to_datetime(data.index)
    return data


def plot_data(data):
    for col in data.columns:
        plot_column(data, col)

def plot_column(data, column='Total', workbook_name=''):
    """ Plot DataFrame """
    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.plot(data.index, data[column])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    plt.title(f'{column} FCN')
    plt.xlabel('Date')
    plt.ylabel('FCN')
    # plt.style.use('seaborn-deep')

    plt.show()
    # plt.savefig(f'{column}_{workbook_name}.png', bbox_inches='tight')


def get_plots_from_workbook(workbook_name):
    data = get_data_frame_from_google_sheet(workbook_name)
    # pprint(data.head())
    # plot_data(data)
    plot_column(data, 'Total', workbook_name)



if __name__ == '__main__':
    # get_plots_from_workbook(FCN_WORKBOOK_NAME)
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    print(len(workbooks))
    # pprint(workbooks[0]['data'], indent=2)
