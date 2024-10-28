import pandas as pd

from src.knit_structure.enums.IncOrDec import IncOrDec
from src.knit_structure.enums.RowsOrRounds import RowsOrRounds
from src.pattern.checker.patternChecker import parse_patt_str, count_sts
from src.pattern.pattSpreadsheetMetadata import PATT_ST_CNT, PATT_NUM_ROWS, PATT_WORKED, PATT_INSTRS, \
    PATT_ROW_ENDING_ST_CNT, PATT_ROW_ENDING_ST_CHANGE_CNT, PATT_ROW_SHAPING
from src.pattern.translatePattern import group_sts_in_row_array, consolidate_repeats_in_row_dict


def read_file_to_dict(_file_name='./2x2 ribbing decrease.xlsx', _sheet_names=None, _read_sheet_name=''):
    '''Reads an xlsx file in the format specified in pattSpreadsheetMetadata.py and translates it to a dictionary for further processing'''
    patt_file = pd.ExcelFile(_file_name)
    sheet_names = patt_file.sheet_names

    patt_data = {}
    for sheet_name in sheet_names:
        a_sheet = pd.read_excel(_file_name, sheet_name)
        patt_data[sheet_name] = a_sheet

    if _read_sheet_name != '':
        apatt_df = patt_data[_read_sheet_name]
    else:
        apatt_df = patt_data[0]

    a_patt_dict = apatt_df.to_dict()
    return a_patt_dict


def build_patt_into_dict_by_rows(col_dict):
    '''Reconstructs the raw pattern dictionary into a dictionary containing metadata about the pattern,
    and a dictionary of the rows (or rnds) of the pattern'''
    patt_dict = {}
    row_dict = {}
    col_keys = []
    if len(col_dict) > 0:
        # Setup Row arrays, numbered
        # Row numbers are in the first column A of spreadsheet
        for col in col_dict:
            col_keys.append(col)

        row_nums = col_dict[col_keys[0]]
        num_rows = len(row_nums)
        patt_dict[PATT_NUM_ROWS] = num_rows
        patt_dict[PATT_WORKED] = RowsOrRounds.from_str(col_keys[0])

        # ! This assumes the format of the spreadsheet has numbered the rows and columns

        for rown in row_nums:
            show_row_num = row_nums[rown]
            row_dict[show_row_num] = [f"{patt_dict[PATT_WORKED].value} {show_row_num}:"]

        # Now pull the pattern into the rows
        for rown in range(0, num_rows):
            for col in range(1, len(col_dict)):
                row_dict[row_nums[rown]].append(col_dict[col][rown])

    # Store how many sts this pattern is worked over (based on numbered columns in spreadsheet)
    patt_dict[PATT_ST_CNT] = len(col_dict) - 1
    patt_dict[PATT_INSTRS] = row_dict

    return patt_dict


def group_sts_into_row_list(patt_row_dict):
    '''Takes the pattern dictionary (with rows/rnds as arrays of instructions)
    Groups individual stitch instructions in the row instructions and removes non-stitches ('nan')s
    Returns updated pattern dictionary '''
    patt_row_instrs = group_sts_in_row_array(patt_row_dict[PATT_INSTRS], patt_row_dict[PATT_WORKED])
    patt_row_dict[PATT_INSTRS] = patt_row_instrs
    return patt_row_dict


def consolidate_repeats_in_patt_dict(patt_row_dict):
    '''
    Takes the pattern dictionary
    Looks to consolidate more repeats in the pattern rows
    Returns the full pattern dictionary, updated
    '''
    consolidated_rep_row_dict = consolidate_repeats_in_row_dict(patt_row_dict[PATT_INSTRS])
    patt_row_dict[PATT_INSTRS] = consolidated_rep_row_dict
    return patt_row_dict


def add_st_cnts_to_rows(patt_dict):
    '''
    Adds metadata of how many sts are left at end of rows in row_dict
    '''
    row_dict = patt_dict[PATT_INSTRS]
    row_cnt_dict = {}
    for arow in row_dict:
        st_cnt = 0
        for patt_instr in row_dict[arow]:
            parsed_patt_str = parse_patt_str(patt_instr)
            st_cnt += count_sts(parsed_patt_str)
        row_cnt_dict[arow] = st_cnt

    patt_dict[PATT_ROW_ENDING_ST_CNT] = row_cnt_dict
    return patt_dict


def determine_st_diff_inc_or_dec(last_st_cnt, st_cnt):
    '''
    Determine if the diff between last_st_cnt and st_cnt resulted in an inc or dec
    Return list of the [<diff_value>, <IncOrDec>]
    '''
    st_diff = last_st_cnt - st_cnt
    if st_diff > 0:  # decrease
        return [st_diff, IncOrDec.DECREASE]
    elif st_diff > 0:  # increase
        st_diff = st_cnt - last_st_cnt
        return [st_diff, IncOrDec.INCREASE]
    return [0, IncOrDec.NONE]


def add_shaping_to_rows(patt_dict):
    '''
    Adds metadata of inc'd or dec'd sts for rows in row_dict
    Requires that the st count dict is set on pattern
    ! Determines this based on diff from count of previous row (i.e. it's not smart enough to look at shaping sts yet)
    '''
    row_dict = patt_dict[PATT_INSTRS]
    row_cnt_dict = patt_dict[PATT_ROW_ENDING_ST_CNT]
    starting_patt_st_cnt = patt_dict[PATT_ST_CNT]
    row_diff_dict = {}
    row_shape_dict = {}
    last_st_cnt = -1

    for arow in row_dict:
        st_cnt = row_cnt_dict[arow]
        if last_st_cnt < 0: # first row
            cnt_diff_shape = determine_st_diff_inc_or_dec(starting_patt_st_cnt, st_cnt)
        else:
            cnt_diff_shape = determine_st_diff_inc_or_dec(last_st_cnt, st_cnt)

        row_diff_dict[arow] = cnt_diff_shape[0]
        row_shape_dict[arow] = cnt_diff_shape[1]

        last_st_cnt = st_cnt

    patt_dict[PATT_ROW_ENDING_ST_CHANGE_CNT] = row_diff_dict
    patt_dict[PATT_ROW_SHAPING] = row_shape_dict
    return patt_dict


def print_patt(patt_dict):
    '''
    Prints the pattern as defined in the pattern dictionary
    '''
    row_dict = patt_dict[PATT_INSTRS]
    row_cnt_dict = patt_dict[PATT_ROW_ENDING_ST_CNT]
    row_diff_dict = patt_dict[PATT_ROW_ENDING_ST_CHANGE_CNT]
    row_shape_dict = patt_dict[PATT_ROW_SHAPING]

    for arow in row_dict:
        if row_cnt_dict.get(arow) and row_diff_dict.get(arow) and row_shape_dict.get(arow):
            print(f"{arow} {row_dict[arow]}. {row_cnt_dict[arow]} sts -- {row_diff_dict[arow]} sts {row_shape_dict[arow].value}.\n")
        elif row_cnt_dict.get(arow):
            print(f"{arow} {row_dict[arow]}. {row_cnt_dict[arow]} sts.\n")
        else:
            print(f"{arow} {row_dict[arow]}.\n")



patt_dict = read_file_to_dict(_file_name='./2x2 ribbing decrease.xlsx', _sheet_names=['Sheet1'], _read_sheet_name='Sheet1')
print(patt_dict)
apatt_row_dict = build_patt_into_dict_by_rows(patt_dict)
apatt_row_dict = group_sts_into_row_list(apatt_row_dict)
consolidated_rep_patt_dict = consolidate_repeats_in_patt_dict(apatt_row_dict)
cnt_patt_dict = add_st_cnts_to_rows(consolidated_rep_patt_dict)
shape_patt_dict = add_shaping_to_rows(cnt_patt_dict)
print_patt(shape_patt_dict)

