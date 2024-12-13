import pandas as pd
import matplotlib.pyplot as plt
import PyPDF2, re


def read_excel_file_into_sheet_dict(_filename):
    sheet_dict = {}
    xfile = pd.ExcelFile(_filename)
    xsheet_names = xfile.sheet_names
    for sheet_name in xsheet_names:
        df_sheet = pd.read_excel(_filename, sheet_name)
        sheet_dict[sheet_name] = df_sheet
    return sheet_dict


def clean_dates_in_df(_df, _df_date_col_name, _printc=False):
    # Clean the dates into dates
    _df[_df_date_col_name] = pd.to_datetime(_df[_df_date_col_name])
    if _printc:
        print(_df.to_string())


dfs_dict = read_excel_file_into_sheet_dict('./G Knitting Projects 2004-2024.xlsx')
for a_sheet in dfs_dict:
    if a_sheet == 'Projects':
        clean_dates_in_df(dfs_dict[a_sheet], 'Started')
        clean_dates_in_df(dfs_dict[a_sheet], 'Completed', True)
    elif a_sheet == 'Mercury Retrogrades':
        clean_dates_in_df(dfs_dict[a_sheet], 'Retrograde Start')
        clean_dates_in_df(dfs_dict[a_sheet], 'Retrograde End', True)

