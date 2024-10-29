import math
import re

PATT_ST_CNT = "Pattern St Cnt:"
PATT_NUM_ROWS = "Pattern Row Cnt:"

def instr_has_num(instr):
    if str(instr) == 'nan':
        return False
    match_str = '.*[0-9]+'
    num_match = re.match(match_str, str(instr))
    if num_match:
        return True
    else:
        return False


def consolidate_repeats(instr_array):
    '''
    Takes an instruction array, tries to combine counts of repeats
    instr_array =
    st_array =
    '''
    # TODO : figure out how to do this
    st_cnt = 0
    st_array = []
    last_st = ''
    for instr in instr_array:
        if last_st == '':  # new st, st_cnt should be 0
            if str(instr) != 'nan':
                last_st = instr
                st_cnt += 1
        elif instr == last_st:  # two of the same in a row, add to cnt
            st_cnt += 1
        else:  # on to a new st
            # add them up if they don't have a num in them already
            if instr_has_num(last_st):
                if st_cnt > 1:
                    st_array.append(f"{last_st} {str(st_cnt)} times")
                else:
                    st_array.append(f"{last_st}")
            else:
                st_array.append(f"{last_st}{str(st_cnt)}")
            if str(instr) != 'nan':
                last_st = instr
                st_cnt = 1  # reset
            else:  # 'nan' means no st, reset and move to the next st
                last_st = ''
                st_cnt = 0

    return st_array


def interpret_row_instr(instr_array):
    '''
    Takes an instruction array, removes nan's, groups repeats
    instr_array = ['k', nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 'k', nan, 'p']
    st_array = ['k2', 'p1']
    '''
    st_cnt = 0
    st_array = []
    last_st = ''
    for instr in instr_array:
        if last_st == '':  # new st, st_cnt should be 0
            if str(instr) != 'nan':
                last_st = instr
                st_cnt += 1
        elif instr == last_st:  # two of the same in a row, add to cnt
            st_cnt += 1
        else:  # on to a new st
            # add them up if they don't have a num in them already
            if instr_has_num(last_st):
                if st_cnt > 1:
                    st_array.append(f"{last_st} {str(st_cnt)} times")
                else:
                    st_array.append(f"{last_st}")
            else:
                st_array.append(f"{last_st}{str(st_cnt)}")
            if str(instr) != 'nan':
                last_st = instr
                st_cnt = 1  # reset
            else:  # 'nan' means no st, reset and move to the next st
                last_st = ''
                st_cnt = 0

    return st_array


def group_sts_in_row_array(row_dict, patt_worked):
    '''Takes Row dictionary of pattern instructions and a RowOrRound enum (patt_worked)
        row_dict format input: {1: ['Rnd 1:', 'k', 'p', 'nan'], 2...}
    Creates a new dictionary of the rows/rnds with the key as the first element of the list
        new_row_dict format output: {'Rnd 1:' : ['k1', 'p1'], 'Rnd 2:' : []...}
    Groups similar, i.e. turns k, k into k2 and removes non-stitches in the array
    Returns the new dictionary
    '''
    new_row_dict = {}
    for arow in row_dict:
        row_instr_array = row_dict[arow]
        if patt_worked.value in row_instr_array[0]:
           # print(row_instr_array[0])  # Print Row X:
            new_row_dict[row_instr_array[0]] = interpret_row_instr(row_instr_array[1:])
    return new_row_dict


def consolidate_list_to_single_instr(ord_list, delim=', '):
    '''Conslidate the ordered list (array) of str instructions into a single str instruction, delimited by delim
    i.e. ['k1', 'p2'] ==> 'k1, p2'
    '''
    single_instr = ""
    if len(ord_list) == 0:
        return ''
    elif len(ord_list) == 1:
        return ord_list[0]
    else:
        for i in range(0, len(ord_list) - 1):
            single_instr += ord_list[i] + delim
        single_instr += ord_list[len(ord_list) - 1]
    return single_instr


def convert_to_repeat(ord_list, rep_ind_l='(', delim=', ', rep_ind_r=')', num_reps=-1, rep_phrase=''):
    '''Take an ordered list (array) of str instructions, and turn it into a single instruction repeating x times.
    i.e. ['k1', 'p1'], 2 ==> ['(k1, p1) 2 times']
    when num_reps == -1, no number shown
    rep_phrase is the phrase to show after num_reps (if included)
    '''
    rep_str = f"{rep_ind_l}{consolidate_list_to_single_instr(ord_list, delim)}{rep_ind_r}"
    if num_reps > 0:
        rep_str += f" {num_reps}"
    if len(rep_phrase) > 0:
        rep_str += f" {rep_phrase}"
    return [rep_str]


def find_repeating_patt_half(ordered_list, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    if len(ordered_list) <= 1:
        # also a stop condition
        return ordered_list
    else:
        # stop condition
        second_haf = len(ordered_list)
        first_half = math.floor(second_haf / 2)
        if ordered_list[0:first_half] == ordered_list[first_half:second_haf]:

            # look for nested repeates in the first half
            rep_half = ordered_list[0:first_half]
            rep_patt_half = find_repeating_patt_half(rep_half)
            new_rep_list = convert_to_repeat(rep_patt_half, rep_phrase=_rep_phrase, num_reps=_num_reps, rep_ind_l=_rep_ind_l, rep_ind_r=_rep_ind_r)

            return new_rep_list
        else:
            return find_repeating_patt_half(ordered_list[0:first_half]) + find_repeating_patt_half(ordered_list[first_half:second_haf])


def find_repeating_patt_forward(ord_list, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    if len(ord_list) <= 1:
        return ord_list
    else:
        if len(ord_list) < 4:
            return ord_list
        else:
            first_two_instr = ord_list[0:2]
            next_two_instr = ord_list[2:4]
            if first_two_instr == next_two_instr:
                # stop condition
               # print("Found a repeat! ", first_two_instr, " == ", next_two_instr)
                new_rep = convert_to_repeat(first_two_instr, num_reps=_num_reps, rep_phrase=_rep_phrase, rep_ind_l=_rep_ind_l, rep_ind_r=_rep_ind_r)
               # print(new_rep)
                return new_rep + find_repeating_patt_forward(ord_list[4:])
            else:
                return [ord_list[0]] + find_repeating_patt_forward(ord_list[1:])


def find_n_repeating_patt_forward_step_forward(ord_list, rep_st_cnt=1, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    if len(ord_list) < rep_st_cnt:
        return ord_list
    else:
        rep_st_cnt_dbld = rep_st_cnt * 2 # two because we'll need this many instrc to find this length rep in
        if len(ord_list) < rep_st_cnt_dbld:
            return ord_list
        else:
            first_chunk = ord_list[0:rep_st_cnt]
            next_chunk = ord_list[rep_st_cnt:rep_st_cnt_dbld]
            if first_chunk == next_chunk:
                # stop condition
                print("Found a repeat! ", first_chunk, " == ", next_chunk)
                new_rep = convert_to_repeat(first_chunk, num_reps=_num_reps, rep_phrase=_rep_phrase, rep_ind_l=_rep_ind_l, rep_ind_r=_rep_ind_r)
                print(new_rep)
                return new_rep + find_n_repeating_patt_forward_step_forward(ord_list[rep_st_cnt_dbld:], rep_st_cnt=rep_st_cnt, _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
            else:  # keep searching forward, expand window
                return [ord_list[0]] + find_n_repeating_patt_forward_step_forward(ord_list[1:], rep_st_cnt=rep_st_cnt, _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)


def find_n_repeating_patt_forward_widening_window(ord_list, rep_st_cnt=1, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    if len(ord_list) < rep_st_cnt:
        return ord_list
    else:
        rep_st_cnt_dbld = rep_st_cnt * 2 # two because we'll need this many instrc to find this length rep in
        if len(ord_list) < rep_st_cnt_dbld:
            return ord_list
        else:
            first_chunk = ord_list[0:rep_st_cnt]
            next_chunk = ord_list[rep_st_cnt:rep_st_cnt_dbld]
            if first_chunk == next_chunk:
                # stop condition
                print("Found a repeat! ", first_chunk, " == ", next_chunk)
                new_rep = convert_to_repeat(first_chunk, num_reps=_num_reps, rep_phrase=_rep_phrase, rep_ind_l=_rep_ind_l, rep_ind_r=_rep_ind_r)
                print(new_rep)
                return new_rep + find_n_repeating_patt_forward_widening_window(ord_list[rep_st_cnt_dbld:], rep_st_cnt=rep_st_cnt, _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
            else:  # keep searching forward, expand window
                return find_n_repeating_patt_forward_widening_window(ord_list, rep_st_cnt=(rep_st_cnt + 1), _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)


def find_reps_n_forward_step(row_dict, _instr_to_rep=1, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    new_row_dict = {}
    for arow in row_dict:
        row_instr = row_dict[arow]
        # now do forward search to find repeats
        rep_instrs = find_n_repeating_patt_forward_step_forward(row_instr, rep_st_cnt=_instr_to_rep, _num_reps=_num_reps, _rep_phrase=_rep_phrase,
                                                                   _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
        new_row_dict[arow] = rep_instrs
    return new_row_dict


def find_reps_n_forward(row_dict, _instr_to_rep=1, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    new_row_dict = {}
    for arow in row_dict:
        row_instr = row_dict[arow]
        # now do forward search to find repeats
        rep_instrs = find_n_repeating_patt_forward_widening_window(row_instr, rep_st_cnt=_instr_to_rep, _num_reps=_num_reps, _rep_phrase=_rep_phrase,
                                                                   _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
        new_row_dict[arow] = rep_instrs
    return new_row_dict


def find_reps_forward(row_dict, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    new_row_dict = {}
    for arow in row_dict:
        row_instr = row_dict[arow]
        # now do forward search to find repeats
        rep_instrs = find_repeating_patt_forward(row_instr, _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
        new_row_dict[arow] = rep_instrs
    return new_row_dict


def find_reps_in_half(row_dict, _num_reps=-1, _rep_phrase="twice", _rep_ind_l="(", _rep_ind_r=")"):
    new_row_dict = {}
    for arow in row_dict:
        row_instr = row_dict[arow]
        # now do forward search to find repeats
        # do it rep_halves times
        rep_instrs = find_repeating_patt_half(row_instr, _num_reps=_num_reps, _rep_phrase=_rep_phrase, _rep_ind_l=_rep_ind_l, _rep_ind_r=_rep_ind_r)
        new_row_dict[arow] = rep_instrs
    return new_row_dict


def consolidate_repeats_in_row_dict(row_dict):
    '''
    Takes the pattern's row dictionary, looks to find repeating patterns and consolidate the instructions
    '''
    new_dict = row_dict
    for n in range(1, len(row_dict)):
        new_dict = find_reps_n_forward(new_dict, n)
        new_dict = find_reps_n_forward_step(new_dict, n)
        if n % 4 == 0:
            new_dict = find_reps_in_half(new_dict)

    #forward_rep_row_dict = find_reps_forward(row_dict)
    #more_forward_rep_row_dict = find_reps_forward(forward_rep_row_dict) #, _num_reps=2, _rep_phrase="times", _rep_ind_l="[", _rep_ind_r="]")


    return new_dict
