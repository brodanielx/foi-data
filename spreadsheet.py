from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from constants import (
    CLIENT_SECRET_FILENAME, FCN_WORKBOOK_NAME, SCOPE
)


def get_google_sheet(workbook_name):
    """ 
    Returns all records of first sheet of workbook in the form of a 
    list of dictionaries 
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRET_FILENAME, SCOPE
        )
    client = gspread.authorize(credentials)

    sheet = client.open(workbook_name).sheet1
    data = sheet.get_all_records()
    return data

def get_data_frame_from_google_sheet(workbook_name):
    data_list = get_google_sheet(workbook_name)
    data = pd.DataFrame(data_list)
    data = clean_data(data)
    return data

def clean_data(data):
    data = data.replace(r'', 0)
    return data


def plot_data(data):
    for col in data.columns:
        plot_column(data, col)

def plot_column(data, column='Tampa'):
    """ Plot DataFrame """
    plt.plot(data['Week'], data[column])

    plt.title(f'{column} FCN')
    plt.xlabel('Week')
    plt.ylabel('FCN')

    plt.show()



if __name__ == '__main__':
    data = get_data_frame_from_google_sheet(FCN_WORKBOOK_NAME)
    # pprint(data, indent=2)
    # plot_data(data)
    plot_column(data)
