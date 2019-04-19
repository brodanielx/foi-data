from pprint import pprint
import smtplib

from constants import (
    DUES_CATEGORY,
    FCN_CATEGORY,
    FOI_CLASS_ATTENDANCE_CATEGORY,
    WORKBOOK_NAME_DICTIONARIES
)

from srk_report_constants import (
    FOI_EMAIL_ADDRESS, FOI_EMAIL_PASSWORD,
    FOOTER_MESSAGE, GREETINGS, SUBJECT,
    SMTP_PORT, SMTP_SERVER
)

from spreadsheet import (
    get_google_workbooks
)

def create_and_send_report():
    email_body_str = create_report()
    send_report(email_body_str)


def create_report():
    workbooks = get_google_workbooks(WORKBOOK_NAME_DICTIONARIES)
    dues_str = get_workbook_values_str(workbooks, DUES_CATEGORY)
    fcn_str = get_workbook_values_str(workbooks, FCN_CATEGORY)
    foi_class_attendance_str = get_workbook_values_str(
        workbooks, FOI_CLASS_ATTENDANCE_CATEGORY
    )

    values_str = f'{dues_str}\n{fcn_str}\n{foi_class_attendance_str}\n'

    email_body_str = f'{GREETINGS}\n{values_str}\n{FOOTER_MESSAGE}'

    return email_body_str

def send_report(email_body_str):
    conn = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    conn.ehlo()
    conn.starttls()
    conn.login(FOI_EMAIL_ADDRESS, FOI_EMAIL_PASSWORD)

    full_email_str = f'Subject: {SUBJECT} 4/18/19\n\n{email_body_str}'

    conn.sendmail(FOI_EMAIL_ADDRESS, FOI_EMAIL_ADDRESS, full_email_str)


def get_workbook_values_str(workbooks, category):
    workbook = next((item for item in workbooks if item['category'] == category), None)
    workbook = handle_dues_data(workbook)
    workbook_data = workbook['data']

    values_str = f'{category}\n'

    for sheet in workbook_data:
        sheet_title = sheet['sheet_title']
        if 'Total' not in sheet_title:
            data = sheet['data']
            data_tail = data.tail(1)
            sheet_values_str = get_sheet_values_str(data_tail)
            values_str += sheet_values_str

    return values_str

def get_sheet_values_str(data_frame):
    sheet_values_str = ''
    series = data_frame.iloc[0]

    for col in data_frame.columns:
        if 'Total' not in col:
            value = series[col]
            value_str = f'{col}: {value}\n'
            sheet_values_str += value_str

    return sheet_values_str

def handle_dues_data(workbook):
    if workbook['category'] == DUES_CATEGORY:
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