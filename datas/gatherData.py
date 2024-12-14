import pandas as pd
import matplotlib.pyplot as plt
import PyPDF2, re
from pandas import Timestamp


def read_excel_file_into_sheet_dict(_filename):
    sheet_dict = {}
    xfile = pd.ExcelFile(_filename)
    xsheet_names = xfile.sheet_names
    for sheet_name in xsheet_names:
        df_sheet = pd.read_excel(_filename, sheet_name)
        sheet_dict[sheet_name] = df_sheet
    return sheet_dict


def clean_dates_in_df(_df, _df_date_col_name, _printc=False, _dropnulls=False):
    # Clean the dates into dates
    _df[_df_date_col_name] = pd.to_datetime(_df[_df_date_col_name])
    if _dropnulls:
        for x in _df.index:
            if pd.isnull(pd.to_datetime(_df.loc[x, _df_date_col_name])):
                if _printc:
                    print("Not a Timestamp", _df.loc[x, _df_date_col_name])
                _df.drop(x, inplace=True)
    if _printc:
        print(_df.to_string())


def calc_retro_ranges(mr_df, _printc=False):
    retro_ranges = []
    for row in mr_df.index:
        retro_start = mr_df.loc[row, 'Retrograde Start']
        retro_end = mr_df.loc[row, 'Retrograde End']
        retro_ranges.append((retro_start, retro_end))
    if _printc:
        print(retro_ranges)
    return retro_ranges


def calc_proj_during_mr(proj_df, retro_ranges, _compare_date_colname, _printc=False):
    proj_during_mr = []
    for row in proj_df.index:
        start_date = proj_df.loc[row, _compare_date_colname]
        for retro_range in retro_ranges:
            if retro_range[0] <= start_date <= retro_range[1]:
                proj_during_mr.append(proj_df.loc[row])
                if _printc:
                    print(proj_df.loc[row, 'Project Name'], _compare_date_colname, " during Mercury Retrograde")

    if _printc:
        print(len(proj_during_mr), " projects ", _compare_date_colname, " during Mercury Retrograde")
        print()
    return proj_during_mr


def calc_proj_started_mr(proj_df, retro_ranges, _printc=False):
    return calc_proj_during_mr(proj_df, retro_ranges, 'Started', _printc)


def calc_proj_completed_mr(proj_df, retro_ranges, _printc=False):
    return calc_proj_during_mr(proj_df, retro_ranges, 'Completed', _printc)


# Work on knitting project and Mercury Retrograde files specifically
dfs_dict = read_excel_file_into_sheet_dict('./G Knitting Projects 2004-2024.xlsx')
for a_sheet in dfs_dict:
    if a_sheet == 'Projects':
        clean_dates_in_df(dfs_dict[a_sheet], 'Started', True, True)
        clean_dates_in_df(dfs_dict[a_sheet], 'Completed', False, False)
    elif a_sheet == 'Mercury Retrogrades':
        clean_dates_in_df(dfs_dict[a_sheet], 'Retrograde Start', True, True)
        clean_dates_in_df(dfs_dict[a_sheet], 'Retrograde End', False, True)

proj_df = dfs_dict['Projects']
mr_df = dfs_dict['Mercury Retrogrades']

mretro_ranges = calc_retro_ranges(mr_df)

proj_started_mr = calc_proj_started_mr(proj_df, mretro_ranges, True)
proj_competed_mr = calc_proj_completed_mr(proj_df, mretro_ranges, True)

# Projects Started during mercury retrograde
# proj_started_mr = proj_df[mr_df['Retrograde Start'] < proj_df['Started']]
# print(proj_started_mr.to_string())
