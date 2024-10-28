import re

def instr_has_num(instr):
    match_str = '.*[0-9]+'
    num_match = re.match(match_str, instr)
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
        if str(instr) != 'nan':
            if last_st == '':  # new st, st_cnt should be 0
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
                st_cnt = 1 # reset
                last_st = instr
        else: # TODO we need to deal with this empty st, likely a result of a dec above



    print(st_array)
    return st_array


def interpret_row_instr_from_dict(row_dict):
    for arow in row_dict:
        #print(arow)
        if arow != "Over Stitches:":
            row_instr_array = row_dict[arow]
            if "Row" in row_instr_array[0]:
                print(row_instr_array[0])  # Print Row X:
                interpret_row_instr(row_instr_array[1:])
