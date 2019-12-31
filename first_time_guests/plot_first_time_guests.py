import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pprint import pprint

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.style as style

from ..constants import (
    COLUMNS_TO_DROP_FOR_HISTOGRAM
)

from data_utils import (
    get_str_date_of_last_row,
    get_list_of_nth_row
)

from first_time_guest_constants import (
    FIRST_TIME_GUESTS_CATEGORY,
    FIRST_TIME_GUESTS_WORKBOOK_NAME_DICTIONARIES
)