# add parent directory to sys.path
import email.utils
import os
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path
cwd = Path(os.getcwd())
parent_dir = str(cwd.parent)
sys.path.append(parent_dir)

from constants.email_constants import (
    FOI_AUTOMATE_EMAIL_ADDRESS,
    FOI_AUTOMATE_EMAIL_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER
)

sender_email = FOI_AUTOMATE_EMAIL_ADDRESS
sender_name = 'FOI Tampa Automation'

recipient_email = 'bro.danielx@gmail.com'
recipient_name = 'Bro Josian X'


def send_email(date):
    print('\nSending FCN Sign Out Sheet email...\n')

    email_text = 'This is a test.'

    message = MIMEText(email_text) 
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))
    message['Subject'] = f'FCN Sign Out Sheet {date}'

    conn = get_smtp_connection()
    conn.sendmail(sender_email, recipient_email, message.as_string())

    print('\nEmail sent.\n')
    pass


def get_smtp_connection():
    conn = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    conn.ehlo()
    conn.starttls()
    conn.login(FOI_AUTOMATE_EMAIL_ADDRESS, FOI_AUTOMATE_EMAIL_PASSWORD)
    return conn





if __name__ == '__main__':
    send_email('12/29/2019')
    pass