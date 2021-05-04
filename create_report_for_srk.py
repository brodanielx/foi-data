import pandas as pd
from pprint import pprint
import smtplib

from constants.constants import (
    DATE_FORMAT,
    DUES_CATEGORY,
    DUES_DISPLAY_TITLE,
    FCN_CATEGORY,
    FOI_CLASS_ATTENDANCE_CATEGORY,
    INACTIVE,
    WORKBOOK_NAME_DICTIONARIES
)

from srk_report_constants import (
    COLUMNS_TO_EXCLUDE,
    FOI_AUTOMATE_EMAIL_ADDRESS, 
    FOI_AUTOMATE_EMAIL_PASSWORD,
    FOI_EMAIL_ADDRESS,
    FOOTER_MESSAGE, GREETINGS, GREETINGS_STPETE,
    RECIPIENT_EMAIL_ADDRESSES, RECIPIENT_EMAIL_ADDRESSES_STPETE,
    SHEET_TITLES_TO_EXCLUDE,
    SUBJECT,
    SMTP_PORT, SMTP_SERVER
)

from spreadsheet import (
    get_google_workbooks
)

def create_and_send_report():
    full_email_str, full_email_str_stpete = create_report()
    send_report(full_email_str, full_email_str_stpete)


def create_report():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    dues_str, dues_str_stpete = get_workbook_values_str(workbooks, DUES_CATEGORY)
    fcn_str, fcn_str_stpete = get_workbook_values_str(workbooks, FCN_CATEGORY)
    foi_class_attendance_str, foi_class_attendance_str_stpete = get_workbook_values_str(
        workbooks, FOI_CLASS_ATTENDANCE_CATEGORY
    )

    date_str = get_report_date(workbooks)

    # values_str = f'{dues_str}\n{fcn_str}\n{foi_class_attendance_str}\n'
    # values_str_stpete = f'{dues_str_stpete}\n{fcn_str_stpete}\n{foi_class_attendance_str_stpete}\n'

    # values_str = f'{dues_str}\n{foi_class_attendance_str}\n'
    # values_str_stpete = f'{dues_str_stpete}\n{foi_class_attendance_str_stpete}\n'

    values_str = f'{dues_str}\n'
    values_str_stpete = f'{dues_str_stpete}\n'

    email_body_str = f'{GREETINGS}{date_str}.\n\n{values_str}\n{FOOTER_MESSAGE}'
    email_body_str_stpete = f'{GREETINGS_STPETE}{date_str}.\n\n{values_str_stpete}\n{FOOTER_MESSAGE}'

    full_email_str = f'Subject: {SUBJECT} {date_str}\n\n{email_body_str}'
    full_email_str_stpete = f'Subject: {SUBJECT} {date_str}\n\n{email_body_str_stpete}'

    return full_email_str, full_email_str_stpete


def send_report(full_email_str, full_email_str_stpete):
    conn = get_smtp_connection()
    conn.sendmail(FOI_AUTOMATE_EMAIL_ADDRESS, RECIPIENT_EMAIL_ADDRESSES, full_email_str)
    conn.sendmail(FOI_AUTOMATE_EMAIL_ADDRESS, RECIPIENT_EMAIL_ADDRESSES_STPETE, full_email_str_stpete)


def get_smtp_connection():
    conn = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    conn.ehlo()
    conn.starttls()
    conn.login(FOI_AUTOMATE_EMAIL_ADDRESS, FOI_AUTOMATE_EMAIL_PASSWORD)
    return conn


def get_report_date(workbooks):
    workbook = next((item for item in workbooks if item['category'] == FOI_CLASS_ATTENDANCE_CATEGORY), None)
    workbook_data = workbook['data']
    sheet1 = workbook_data[0]
    sheet1_data = sheet1['data']
    data_tail = sheet1_data.tail(1)
    date = data_tail.index.values[0]
    timestamp = pd.to_datetime(str(date))
    date_str = timestamp.strftime(DATE_FORMAT)
    return date_str



def get_workbook_values_str(workbooks, category):
    workbook = next((item for item in workbooks if item['category'] == category), None)
    workbook = handle_dues_data(workbook)
    workbook_data = workbook['data']
    category = workbook['category']

    values_str = f'{category}\n'
    values_str_stpete = f'{category}\n'

    for sheet in workbook_data:
        sheet_title = sheet['sheet_title']
        
        if sheet_title != 'Total':
            data = sheet['data']
            data_tail = data.tail(1)
            sheet_values_str = get_sheet_values_str(data_tail)

            if sheet_title == 'StPete':
                values_str_stpete += sheet_values_str
            else:
                values_str += sheet_values_str
        elif sheet_title == 'Total':
            data = sheet['data']
            most_recent_week = data.tail(1).iloc[0]

            total = most_recent_week['Total']
            total_stpete = most_recent_week['StPete']

            total_str = f'Total: {total}\n'
            total_stpete_str = f'Total: {total_stpete}\n'

    values_str += total_str
    values_str_stpete += total_stpete_str

    return values_str, values_str_stpete

def get_sheet_values_str(data_frame):
    sheet_values_str = ''
    series = data_frame.iloc[0]
    series = series[series != 0]

    for col in series.index:
        if col not in (COLUMNS_TO_EXCLUDE + INACTIVE):
            value = series[col]
            value_str = f'{col}: {value}\n'
            sheet_values_str += value_str

    return sheet_values_str

def handle_dues_data(workbook):
    if workbook['category'] == DUES_CATEGORY:
        workbook['category'] = DUES_DISPLAY_TITLE
        workbook_data = workbook['data']
        for sheet in workbook_data:
            data = sheet['data']
            for col in data.columns:
                data.loc[:, col] /= 2
            sheet['data'] = data
        
        workbook['data'] = workbook_data
    
    return workbook


if __name__ == '__main__':
    create_and_send_report()