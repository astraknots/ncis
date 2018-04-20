#!/usr/bin/python

import logging, re
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def convert_pattern_from_web(txtfilename):
    '''Utility fcn to translate the repeating instructions to the format I want to store'''
    # Open the file for reading as text
    patfile = open(txtfilename, 'r')
    patlines = patfile.readlines()
    rows = storeRowsInDict(patlines)
    #print(rows)

    # Loop over the rows of the pattern, replacing dict items with repeats; i.e. "Rep Row x" - should prolly do this first
    for rownum, rowinstr in rows.items():
        logging.debug("instr:")
        logging.debug(rowinstr)
        rowRep = rowRepeatingAnotherRow(rowinstr)
        logging.debug("rowRep:")
        logging.debug(rowRep)
        if rowRep != -1:
            logging.debug(rows[int(rowRep)])
            rows[rownum] = replace_rep_row(rowinstr, rows[int(rowRep)])


    #Look for instr that repeat like 'Rows 3 and 4:'


    # Loop over the rows and add in details for any missing rows; i.e. "and all other odd rows"
    try:
        if first_row_repeats_odd(rows[1]) and row_missing_instr(rows[3]):
            # For now we're assuming if the word odd is in the first row instr, and some odd rows are missing instructions, to rep 1st row for odd
            for rownum, rowinstr in rows.items():
                if rownum != 1 and rownum % 2 != 0:
                    logging.debug(rows[1])
                    rows[rownum] = replace_row_with_num_instr(rownum, rows[1])
                    logging.debug("m odd instr:")
                    logging.debug(rowinstr)
        elif second_row_repeats_even(rows[1]) and row_missing_instr(rows[2]):
            # For now we're assuming if the word even is in the second row instr, and some even rows are missing instructions, to rep 2nd row for even
            for rownum, rowinstr in rows.items():
                if rownum > 2 and rownum % 2 == 0:
                    logging.debug(rows[2])
                    rows[rownum] = replace_row_with_num_instr(rownum, rows[2])
                    logging.debug("m even instr:")
                    logging.debug(rowinstr)
    except:
        logging.error("Something went wrong")

    # Loop over the rows and add in any missing rows that are specified; i.e. "Rows 2,4,6:"



    # Print out the transformed pattern as a dict list
    pat = {}  #Create dict format
    patrows = rows.values() # Get each of the rows into list format
    logging.debug(patrows)
    pat[rows[0]] = patrows[1:]  # make the name of the pattern the key to the dict and the list of rows the value
    # Print
    logging.info(pat)

    #Write the new pat back to a file
    txtfilenamenew = str(txtfilename).replace('.txt', 'new.txt')
    newpatfile = open(txtfilenamenew, 'w')
    newpatfile.writelines(str(pat))
    newpatfile.close()

    patfile.close()


def replace_row_with_num_instr(rowNum, rowInstr):
    '''Return the new row instru to contain the rowNum given'''
    rowIdx = rowInstr.index(':')
    endNewRowInstr = rowInstr[rowIdx+1:]
    logging.debug(endNewRowInstr)
    return "Row " + str(rowNum) + ":" + endNewRowInstr


def first_row_repeats_odd(rowOneInstr):
    '''Returns True if the first row instruction contains the word odd'''
    if "odd" in rowOneInstr:
        # Possibly a repeating odd row instruction
        logging.info("Possibly a repeating odd row instr:" + rowOneInstr)
        return True
    return False


def second_row_repeats_even(rowTwoInstr):
    '''Returns True if the first row instruction contains the word even'''
    if "even" in rowTwoInstr:
        # Possibly a repeating even row instruction
        logging.info("Possibly a repeating even row instr:" + rowTwoInstr)
        return True
    return False


def row_missing_instr(row):
    '''Returns True if the only instr is the Row number'''
    rowpieces = row.split(' ')
    if len(rowpieces) == 3 and rowpieces[0] == "Row" and len(rowpieces[2]) == 0:
        logging.info("Missing instr for " + row)
        return True
    return False


def replace_rep_row(rowinstr, replaceWithRowInstr):
    '''Replace the 'Rep Row x' with the instruction replaceWithRowInstr'''
    logging.debug(rowinstr)
    logging.debug(replaceWithRowInstr)
    ogRow = rowinstr.split(':')
    newRow = replaceWithRowInstr.split(':')
    logging.debug(ogRow)
    logging.debug(newRow)

    replacedRowInstr = ogRow[0] + ":" + newRow[1]

    if len(newRow) > 2:
        raise ValueError("More row instructions were not concatonated")

    logging.debug(replacedRowInstr)
    return replacedRowInstr


def rowRepeatingAnotherRow(rowinstr):
    '''Return row this row instruction is trying to repeat, otherwise -1 if this row isn't repeating another row. '''
    if "Rep Row" in rowinstr:
        rowWords = rowinstr.split(' ')
        repIdx = rowWords.index("Rep")
        rowToRep = rowWords[repIdx+2]  # Adding 2 'cause it should be 'Rep', 'Row', '<row num we want>'
        logging.debug(rowToRep)
        return rowToRep

    return -1


def storeRowsInDict(patlines):
    '''Take lines read in from file and store each in a dict by Row num, Row 0 is the name of the pattern'''
    rows = {}
    cntr = 0
    for line in patlines:
        logging.debug("line:" + line)
        rowlist = line.split('\n')
        logging.debug("Raw rowsplit:")
        logging.debug(rowlist)
        for piece in rowlist:
            if piece:
                # Get the Row num in the piece
                rowinstr = piece
                rowNum = get_row_num_from_instr(rowinstr)
                if rowNum != str(cntr):
                    # Loop over, filling in missing rows until we get to the right number
                    for x in range(cntr, int(rowNum)):
                        logging.info("Row num missing: rowNum:" + rowNum + " cntr:" + str(cntr))
                        rows[cntr] = "Row " + str(cntr) + ": "
                        cntr += 1
                    # Now we should have the matching row, add it as well
                rows[cntr] = piece
                cntr += 1
        logging.debug(rows)
    return rows


def get_row_num_from_instr(row_instr):
    '''Return the row num in this instruction, or if mult are listed, the first one; i.e. Rows 2,4,6 would return 2; if not found returns -1'''
    row_num = get_num_from_next_word_after_term(row_instr, "Row")
    if row_num == -1:
        row_num = get_num_from_next_word_after_term(row_instr, "Rows")

    return row_num


def get_num_from_next_word_after_term(sentence, searchTerm):
    '''Get a number in the sentence following the word searchTerm; else return -1'''
    next_word = get_next_word_after_term(sentence, searchTerm, " ")
    if next_word:
        return get_just_number(next_word)
    return -1


def get_next_word_after_term(sentence, searchTerm, splitter):
    '''Splits sentence on splitter, then gives you the word after the searchTerm; returns empty string '''
    word_list = sentence.split(splitter)
    try:
        search_term_idx = word_list.index(searchTerm)
    except ValueError:
        logging.warning("searchTerm:" + searchTerm + " was not found in sentence:" + sentence)
        return ''

    next_word_idx = search_term_idx + 1
    if next_word_idx >= len(word_list):
        logging.warning("searchTerm:" + searchTerm + " was the last word in sentence:" + sentence)
        return ''
    return word_list[next_word_idx]  # Adding 1 'cause it should be 'Row', '<row num we want>:'


def get_just_number(word_str_w_number):
    '''Searches the wordStr for a number and strips out anything non-numeric; returns number as a string, or empty string if no number found'''
    return str(re.sub("[^0-9]", "", word_str_w_number))