import pandas as pd

from src.pattern.translatePattern import group_sts_in_row_array, consolidate_repeats_in_row_dict


#from pathLib import Path
#import lxml, html5lib, beautifulsoup4

#dfAstraFall = pandas.read_csv('./Astrology Knitting Dignity - Fall.csv')

#print(dfAstraFall)
#p = Path(__file__).parents[1]
#print(p)


def read_file_to_dict(_file_name='', _sheet_names=None, _read_sheet_name=''):

    pattFile = pd.ExcelFile(_file_name)
    sheet_names = pattFile.sheet_names

    pattData = {}
    for sheet_name in sheet_names:
        a_sheet = pd.read_excel('./2x2 ribbing decrease.xlsx', sheet_name)
        pattData[sheet_name] = a_sheet

    if _read_sheet_name != '':
        apatt_df = pattData[_read_sheet_name]
    else:
        apatt_df = pattData[0]

    a_patt_dict = apatt_df.to_dict()
    return a_patt_dict


def build_row_dict(col_dict):
    row_dict = {}
    col_keys = []
    if len(col_dict) > 0:
        # Setup Row arrays, numbered
        # Row numbers are in the first column A of spreadsheet
        for col in col_dict:
            col_keys.append(col)
            #print(col)
        row_nums = col_dict[col_keys[0]]
        num_rows = len(row_nums)
        print('\nNum rows', num_rows)
        print('Row nums', row_nums)
        for rown in row_nums:
            show_row_num = row_nums[rown]
            row_dict[show_row_num] = [f"Row {show_row_num}:"]
    #    print("\nRow Dict:", row_dict)

        # Now pull the pattern into the rows
        for rown in range(0, num_rows):
            for col in range(1, len(col_dict)):
                row_dict[row_nums[rown]].append(col_dict[col][rown])

    '''    print("\nRows of row dict:")
        for arow in row_dict:
            print(row_dict[arow])   '''

    row_dict["Over Stitches:"] = len(col_dict) - 1

    return row_dict


patt_dict = read_file_to_dict(_file_name='./2x2 ribbing decrease.xlsx', _sheet_names=['Sheet1'], _read_sheet_name='Sheet1')
print(patt_dict)
patt_row_dict = build_row_dict(patt_dict)
print("\nInterpreted into instructions:\n")
new_row_dict = group_sts_in_row_array(patt_row_dict)

print(new_row_dict)
consolidate_repeats_in_row_dict(new_row_dict)

