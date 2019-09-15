from constants import (
    TOTAL_SHEET_TITLE
)

def get_non_total_sheets_by_category(workbooks, category):
    workbook_data = get_workbook_data_by_category(workbooks, category)

    sheets = get_sheets_by_sheet_title_not_equal_to_title(workbook_data, TOTAL_SHEET_TITLE)

    return sheets

def get_data_frame_by_category_and_sheet_title(workbooks, category, sheet_title):
    workbook_data = get_workbook_data_by_category(workbooks, category)

    sheet = get_sheet_by_title(workbook_data, sheet_title)

    return get_sheet_data(sheet)

def get_workbook_data_by_category(workbooks, category):
    workbook = filter_workbook_dictionary_by_category(workbooks, category)

    return get_workbook_data(workbook)


def get_index(data_frame):
    return data_frame.index


def get_series_by_column_title(data_frame, column_title):
    return data_frame[column_title]


def filter_workbook_dictionary_by_category(workbooks, category):
    return [workbook for workbook in workbooks if workbook['category'] == category][0]

def get_workbook_data(workbook):
    return workbook['data']

def get_sheet_by_title(workbook_data, sheet_title):
    return [sheet for sheet in workbook_data if sheet['sheet_title'] == sheet_title][0]

def get_sheets_by_sheet_title_not_equal_to_title(workbook_data, title):
    return [sheet for sheet in workbook_data if sheet['sheet_title'] not in [title, 'StPete']]

def get_sheet_data(sheet):
    return sheet['data']

def add_goal_column(data_frame, goal_value):
    data_frame['Goal'] = goal_value

def get_goal_column(data_frame):
    return data_frame.Goal

def slice_data_frame_by_tail(data_frame, row_count):
    row_count *= -1
    data_frame = data_frame.iloc[row_count:]
    return data_frame

def slice_data_frames_by_tail(data_frame1, data_frame2, row_count):
    row_count *= -1
    data_frame1 = data_frame1.iloc[row_count:]
    data_frame2 = data_frame2.iloc[row_count:]
    return data_frame1, data_frame2
