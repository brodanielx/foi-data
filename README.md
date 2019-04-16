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



get_google_sheet() => get_google_workbook()
    - returns list of dictionaries
    - each dictionary
        - {
            'sheet_title': sheet_title,
            'data': [list]
        }