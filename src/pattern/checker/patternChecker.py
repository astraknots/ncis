#!/usr/bin/python

import getopt
import logging
import sys
import re
import json

SEPARATORS = [',', '.']
REPEAT_START = ['(', '[', '*']
REPEAT_END = [')', ']', '*']
REPEAT_WORDS = {'ONCE': 1, 'TWICE': 2}
OPERATION_CNT = {'K': 1, 'P': 1, 'SM': 0, 'YO': 1, '2TOG': 1}


def get_rep_end_for_start(rep_start_str):
    if rep_start_str in REPEAT_START:
        idx = REPEAT_START.index(rep_start_str)
        return REPEAT_END[idx]


def determine_rep_reps(rep_patt_instr_str):
    '''Determine the number of times to execute a repeat from a patt instru. i.e. 2 times or Twice or x 2'''
    print(rep_patt_instr_str)
    rep_words = rep_patt_instr_str.split(' ')
    for rep_word in rep_words:
        if len(rep_word) > 0:
            if rep_word.isnumeric():
                return int(rep_word)
            else:
                rep_word_u = rep_word.upper()
                if rep_word_u in REPEAT_WORDS:
                    return REPEAT_WORDS[rep_word_u]

    return 1


def parse_patt_str(patt_str, skip_repeat=False):
    instrs = []
    single = ''

    # Loop over each char in the instr str
    for idx in range(0, len(patt_str)):
        char = patt_str[idx]

        # if we have the beginning of a repeat character
        if not skip_repeat and char in REPEAT_START:
            # get the rest of the str after that char
            rem_patt_str = patt_str[idx + 1:]
            # find the index of the end of repeat char in remaining str
            rep_end_idx = rem_patt_str.find(get_rep_end_for_start(char), 1)
            # parse the instructions for repeat - makes a recursive call that will skip this section, thus skip_repeat = True
            rep_instrs = parse_patt_str(rem_patt_str[0:rep_end_idx], True)
            # get index of the end of repeat
            end_rep_instru_idx = rem_patt_str.find(SEPARATORS[0], rep_end_idx)

            # capture the remaining patt str to parse
            remain_patt_str = ''
            # determine how many times this should repeat
            if end_rep_instru_idx == -1: # we've just hit end of str
                rep_reps = determine_rep_reps(rem_patt_str[rep_end_idx + 1:])
            else:
                rep_reps = determine_rep_reps(rem_patt_str[rep_end_idx + 1:end_rep_instru_idx])
                remain_patt_str = rem_patt_str[end_rep_instru_idx + 1:]
            # Add the instrs repeated out as individual instructions
            added = 0
            while (added < rep_reps):
                instrs.extend(rep_instrs)
                added += 1

            # recursively call this on the rem_patt_str after this repeat, and extend the result
            if len(remain_patt_str) > 0:
                instrs.extend(parse_patt_str(remain_patt_str))
            break

        elif char in SEPARATORS:
            # when we hit a separator (i.e. ,) we've gathered a whole instruction, add to array
            instrs.append(single.strip())
            single = ''
            continue
        else:
            # gather another character of an instruction
            single += char

    # This captures the last fully gathered instruction, once we've run out of separators that indicate the end
    if len(single.strip()) > 0:
        instrs.append(single.strip())

    print(instrs)  # debug
    return instrs


def get_num_from_str(a_str):
    # get the numbers of the instr
    match_str = '[0-9]$'
    a_cnt_search = re.search(match_str, a_str)
    # print("A patt has cnt:", a_cnt_search)
    a_cnt_list = re.findall(match_str, a_str)
    # print("A cnt:", a_cnt_list)
    if a_cnt_list and len(a_cnt_list) > 0:
        st_cnt = 0
        for a_cnt in a_cnt_list:
            st_cnt += int(a_cnt)
        return st_cnt
    return 0


def count_instr_sts(instr):
    cnt = 0
    if instr in ['SM', 'PM', 'RM']:
        cnt += 0
    elif instr in ['YO']:
        cnt += 1
    elif instr in ['SSK']:
        cnt += 1
    elif instr in ['K2TOG']:
        cnt += 1
    elif instr in ['K', 'P']:
        cnt += 1
    else:
        cnt += get_num_from_str(instr)

    print(f"{instr} has {cnt} st{'s' if cnt > 1 else ''}")
    return cnt


def count_sts(patt_instr_list, specials=None):
    '''Count the number of sts this list of instrs involves - gives the count AFTER executing the sts'''
    if specials is None:
        specials = []
    total_cnt = 0

    for patt_instr in patt_instr_list:
        match = False
        if len(specials) > 0:
            for special in specials:
                if patt_instr == special["stitch-name"]:
                    cnt = special["stitch-count"]
                    total_cnt += cnt
                    print(f"{patt_instr} has {cnt} st{'s' if cnt > 1 else ''}")
                    match = True

        if not match:
            total_cnt += count_instr_sts(patt_instr.upper())

    return total_cnt


'''    
    st_cnt = 0
    print(patt_str)
    # split the patt str by comma
    patt_pie = patt_str.split(',')
    print(patt_pie)
    for a_patt in patt_pie:
        print("-----A patt: ", a_patt)
        # try to count, or see if it is longer
        if "TWICE" in a_patt:
            print(a_patt, " Contains repeat Twice")
        elif "TIMES" in a_patt:
            print(a_patt, " Contains repeat Times")
        else:
            # see if part of a rep
            if '(' in a_patt:
                print(a_patt, " Begins rep")
            elif ')' in a_patt:
                print(a_patt, " Ends rep")

        # get the numbers of the instr
        match_str = '[0-9]$'
        a_cnt_search = re.search(match_str, a_patt)
        print("A patt has cnt:", a_cnt_search)
        a_cnt_list = re.findall(match_str, a_patt)
        print("A cnt:", a_cnt_list)
        if a_cnt_list and len(a_cnt_list) > 0:
            for a_cnt in a_cnt_list:
                print("..adding ", a_cnt, " to ", st_cnt)
                st_cnt += int(a_cnt)

    return st_cnt
'''


def parse_special_patt_instrs(filename):
    '''Expected format for special pattern instru:
    { "stitch-name": <str stitch-name> i.e. "LC",
      "instr": <str normal separated list of knit instructions> i.e. "sl 1 st to cable needle and hold in front, k2, k1 from cable needle",
      "stitch-count": <int number of sts included in this special stitch> i.e. 3
      (optional) "separator": <str separator> i.e. ','
    }
    TOdo: For patterns? inc row instrs -- see/leverage patternUtil
    '''
    specials = [] # list of dictionaries of json read in
    # Read in the file
    raw_data = ""
    with open(filename) as f:
        for line in f:
            raw_data += line
            if '}' in line: # then we've reached the end of this, parse and store
                # parse from json format into python dict
                data = json.loads(raw_data)
                specials.append(data)
                raw_data = ""

    for item in specials:
        print(item)
        #print(item, "=", data[item])

    # print(json.dumps(data))
    return specials


def check_pattern(argv):
    filename = ''
    patt_str = ''
    try:
        opts, args = getopt.getopt(argv, "hp:f:b:", ["patt=", "file="])
    except getopt.GetoptError:
        print('patternChecker.py -p <pattern-str> -f <pattern-file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('patternChecker.py -p <pattern-str> -f <pattern-file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-p", "--patt"):
            patt_str = arg.upper()
        elif opt in "-b":
            patt_str = ''

    if filename == '':
        logging.info("No filename of pattern given")
        specials = []
    else:
        logging.info("Filename of pattern given:" + filename)
        specials = parse_special_patt_instrs(filename)

    if patt_str == '':
        logging.info("No pattern string given")
        return

    parsed_instr = parse_patt_str(patt_str)
    st_cnt = count_sts(parsed_instr, specials)
    print("Found a total stitch count of:", st_cnt)


if __name__ == "__main__":
    check_pattern(sys.argv[1:])
