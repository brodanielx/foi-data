# FOI Data


## Secretary Report
1. Get data from google sheets
    - format sheet for DataFrame
    - Load data from each sheet into a DataFrame
        - https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e
    - Get date needed for report
2. Compile email
3. Send email

## ToDo
- send weekly FOI report to SRK
    - create report
        - get data from all (3) google sheets


## ToDo
- save graphs to a folder
- see todo_040419.jpg
- add date to plot file names
- separate functions
    - googlesheets.py
    - lineplots.py
    - barplots.py
- get plots for FCN, Dues, Attendance



workbooks = [workbook1, workbook2,...] => list of dictionaries
workbook1 = {
    'category' : 'category',
    'data' : workbook_data
}
workbook_data = [sheet1, sheet2,...] => list of dictionaries
sheet1 = {
    'sheet_title' : sheet_title,
    'data' : data
}
data = dataframe