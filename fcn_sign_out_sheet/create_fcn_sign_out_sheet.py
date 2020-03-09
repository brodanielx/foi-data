# add parent directory to sys.path
import os
import sys
from pathlib import Path
cwd = Path(os.getcwd())
parent_dir = str(cwd.parent)
sys.path.append(parent_dir)

from reportlab.pdfgen import canvas

import plot_fcn_bar as fcn
import data_utils as utils 

signature_underline = '_'*18
ten_spaces = ' '*10
twelve_spaces = ' '*12
twenty_spaces = ' '*20


def create_sign_out_pdf(df, date):

    data_series = clean_data(df)

    file_name = f'FCNSignOut{date}.pdf'.replace('/', '')
    title = f'FCN Sign Out {date}'

    pdf = create_blank_pdf(file_name, title)

    draw_title(pdf, title)

    draw_column_headers(pdf)

    draw_sign_out_lines(pdf, data_series)

    pdf.save()

    pass


def clean_data(df):
    # df.drop(columns='12186 - Chad Muhammad', inplace=True)
    df.rename(columns = lambda col: utils.get_column_name_display(col), inplace=True)

    series = df.squeeze()
    series = series[series > 0]
    series.sort_values(ascending=False, inplace=True)
    return series


def create_blank_pdf(file_name, title):
    pdf = canvas.Canvas(file_name)
    pdf.setTitle(title)
    # draw_ruler(pdf)
    
    return pdf 

def draw_title(pdf, title):
    pdf.setFont('Courier-Bold', 36)
    pdf.drawCentredString(300, 770, title)
    pass


def draw_column_headers(pdf):
    column_headers_str = f'FOI{twelve_spaces}FCN{ten_spaces}Signature'
    pdf.setFont('Courier', 18)
    pdf.drawCentredString(300, 670, column_headers_str)

    pass


def draw_sign_out_lines(pdf, data_series):
    pdf.setFont('Courier', 14)
    y_pos = 650
    for name, value in data_series.iteritems():
        if y_pos > 0:
            value_str = str(value)

            pdf.drawString(50, y_pos, name)
            pdf.drawString(270, y_pos, value_str)
            pdf.drawString(400, y_pos, signature_underline)

            y_pos -= 20

        else:
            print('Page full. Create new page.')

    pass 


def draw_ruler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')



if __name__ == '__main__':
    # create_sign_out_pdf()
    pass