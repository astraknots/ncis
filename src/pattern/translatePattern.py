import re


def instr_has_num(instr):
    if str(instr) == 'nan':
        return False
    match_str = '.*[0-9]+'
    num_match = re.match(match_str, str(instr))
    if num_match:
        return True
    else:
        return False


def interpret_row_instr(instr_array):
    print("Rewriting:", instr_array)

    st_cnt = 0
    st_array = []
    last_st = ''
    for instr in instr_array:
        if last_st == '':  # new st, st_cnt should be 0
            if str(instr) != 'nan':
                last_st = instr
                st_cnt += 1
            #print('new st:', last_st, str(st_cnt))
        elif instr == last_st: # two of the same in a row, add to cnt
            st_cnt += 1
            #print("two in a row:", last_st, str(st_cnt))
        else: # on to a new st
            # add them up if they don't have a num in them already
           # print("on to next st, last st:", last_st, str(st_cnt))
            if instr_has_num(last_st):
                if st_cnt > 1:
                    st_array.append(f"{last_st} {str(st_cnt)} times")
                else:
                    st_array.append(f"{last_st}")
            else:
                st_array.append(f"{last_st}{str(st_cnt)}")
            #print("updated st_array to:", st_array)
            if str(instr) != 'nan':
                last_st = instr
                st_cnt = 1  # reset
            else: # 'nan' means no st, reset and move to the next st
                last_st = ''
                st_cnt = 0

    print("Into:", st_array)
    return st_array


def group_sts_in_row_array(row_dict):
    new_row_dict = {}
    for arow in row_dict:
        #print(arow)
        if arow != "Over Stitches:":
            row_instr_array = row_dict[arow]
            if "Row" in row_instr_array[0]:
                print(row_instr_array[0])  # Print Row X:
                new_row_dict[row_instr_array[0]] = interpret_row_instr(row_instr_array[1:])
    return new_row_dict


#def find_repeating_patt(ordered_list):


def consolidate_repeats_in_row_dict(row_dict):
    new_row_dict = {}
    for arow in row_dict:
        row_instr = row_dict[arow]
        # look for repeating patterns and turn into repeat instruction
        print("Can we consolidate?", row_instr)
        # Do the first two instr match?
        if row_instr[0] == row_instr[1]:
            print("We've got a repeat!", row_instr[0], " == ", row_instr[1])
            # TODO this is the start of our recursive fcn...
        # first let's combine the first 2 instr and see if that repeats,
        # already assuming due to our previous grouping at this point we have no repeats --> not true
        if len(row_instr) > 3:  # and the array has to be longer than 3 instructions for this to be possible
            first_group = row_instr[0:2]
            print("first group:", first_group)
        else:
            print("Nope, array was only ", len(row_instr), " long.")
