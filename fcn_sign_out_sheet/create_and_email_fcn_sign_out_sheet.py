
# add parent directory to sys.path
import os
import sys
from pathlib import Path
cwd = Path(os.getcwd())
parent_dir = str(cwd.parent)
sys.path.append(parent_dir)

import plot_fcn_bar as fcn
from create_fcn_sign_out_sheet import create_sign_out_pdf

def create_and_email_fcn_sign_out_sheet():

    df, date = fcn.get_data_and_date()

    create_sign_out_pdf(df, date)

    pass









if __name__ == '__main__':
    create_and_email_fcn_sign_out_sheet()
    pass