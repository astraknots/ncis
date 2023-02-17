#!/usr/bin/python
import getopt
import logging, re
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def read_pattern_from_text(txtfilename):
    '''Util fcn to '''
    patfile = open(txtfilename, 'r')
    patlines = patfile.readlines()
    meta, rnds = covert_rnds_to_instr_dict(patlines)
    # Get pattern name (firstline)
    pattname = rnds[0]
    print(pattname)
    print(rnds)
    print(meta)


def check_line_for_metadata(line):
    '''Check to see if the line str contains the pattern metadata. Return num of lines of metadata'''
    meta_found = 0
    meta_found += search_word_in_line(line, "multiple")
    meta_found += search_word_in_line(line, "odd")
    meta_found += search_word_in_line(line, "Odd")
    meta_found += search_word_in_line(line, "any")
    meta_found += search_word_in_line(line, "Any")
    meta_found += search_word_in_line(line, "even")
    meta_found += search_word_in_line(line, "Even")
    meta_found += search_word_in_line(line, "Multiple")
    return meta_found


def process_metadata(pattname, line):
    '''Pull the metadata of a pattern into its own dict'''
    meta = {}
    metadata = {}
    # split on ;
    meta_parts = line.split(';')
    metadata['STS'] = meta_parts[0]
    metadata['RNDS'] = meta_parts[1]
    meta[pattname] = metadata
    return meta


def covert_rnds_to_instr_dict(patlines):
    '''Take lines read in from file and store each in a dict by Rnd num, Rnd 0 is the name of the pattern. Doesn't include subtitle metadata about pattern'''
    rnds = {}
    meta = {}
    cntr = 0
    skip_lines = 0
    for line in patlines:
        logging.debug("line:" + line)
        if cntr == 1 and check_line_for_metadata(line) > 0:
            # skip_lines += 1
            # process metadata here
            meta = process_metadata(rnds[0], line)
            continue
        rndlist = line.split('\n')
        logging.debug("Raw rndsplit:")
        logging.debug(rndlist)
        innerCnt = 0
        for piece in rndlist:
            if piece:
                # Get the Rnd num in the piece
                rndinstr = piece

                if cntr > skip_lines:
                    rndNums = get_rnd_nums_from_instruction(rndinstr)

                    # Strip out the "Rnd x:" of the instruction to get just the instruction
                    instr_stripped = str(rndinstr.split(': ')[1:]).strip()
                    if len(rndNums) > 1:
                        start = 0
                        end = 1
                        for rndNum in rndNums:
                            if start == 0:
                                start = int(rndNum)
                            else:
                                end = int(rndNum)
                        for rndCnt in range(start, end + 1):
                            rnds[rndCnt] = instr_stripped
                            innerCnt += 1
                    elif rndNums[0] == str(cntr):
                        rnds[cntr] = instr_stripped
                    else:
                        rnds[rndNums[0]] = instr_stripped
                else:
                    rnds[cntr] = piece
                cntr += 1
        logging.debug(rnds)
    return meta, rnds


def covert_rnds_to_dict(patlines):
    '''Take lines read in from file and store each in a dict by Rnd num, Rnd 0 is the name of the pattern'''
    rnds = {}
    cntr = 0
    for line in patlines:
        logging.debug("line:" + line)
        rndlist = line.split('\n')
        logging.debug("Raw rndsplit:")
        logging.debug(rndlist)
        for piece in rndlist:
            if piece:
                # Get the Rnd num in the piece
                rndinstr = piece
                rndNum = get_rnd_num_from_instruction(rndinstr)
                if rndNum != str(cntr):
                    # Loop over, filling in missing rows until we get to the right number
                    for x in range(cntr, int(rndNum)):
                        logging.info("Rnd num missing: rndNum:" + rndNum + " cntr:" + str(cntr))
                        rnds[cntr] = "Rnd " + str(cntr) + ": "
                        cntr += 1
                    # Now we should have the matching row, add it as well
                rnds[cntr] = piece
                cntr += 1
        logging.debug(rnds)
    return rnds


def get_rnd_nums_from_instruction(rndinstr):
    '''Return the rnd nums in this instruction. If only 1 list is length 1, else length 0 or more than 1'''
    rndNums = []
    rndNums = get_num_from_next_word_after_term(rndinstr, "Rnd")
    if rndNums == -1:
        rndNums = get_num_from_next_word_after_term(rndinstr, "Rnds")
    if rndNums == -1:
        rndNums = get_num_from_next_word_after_term(rndinstr, "Round")
    if rndNums == -1:
        rndNums = get_num_from_next_word_after_term(rndinstr, "Rounds")

    return rndNums


def get_rnd_num_from_instruction(rndinstr):
    '''Return the rnd num in this instruction, or if mult are listed, the first one; i.e. Rnds 2,4,6 would return 2; if not found returns -1'''
    rndNum = getNumFromNextWordAfterTerm(rndinstr, "Rnd")
    if rndNum == -1:
        rndNum = getNumFromNextWordAfterTerm(rndinstr, "Rnds")
    if rndNum == -1:
        rndNum = getNumFromNextWordAfterTerm(rndinstr, "Round")
    if rndNum == -1:
        rndNum = getNumFromNextWordAfterTerm(rndinstr, "Rounds")

    return rndNum


def convertPatternFromWeb(txtfilename):
    '''Utility fcn to translate the repeating instructions to the format I want to store'''
    # Open the file for reading as text
    patfile = open(txtfilename, 'r')
    patlines = patfile.readlines()
    rows = storeRowsInDict(patlines)
    # print(rows)

    # Loop over the rows of the pattern, replacing dict items with repeats; i.e. "Rep Row x" - should prolly do this first
    for rownum, rowinstr in rows.items():
        logging.debug("instr:")
        logging.debug(rowinstr)
        rowRep = rowRepeatingAnotherRow(rowinstr)
        logging.debug("rowRep:")
        logging.debug(rowRep)
        if rowRep != -1:
            logging.debug(rows[int(rowRep)])
            rows[rownum] = replaceRepRow(rowinstr, rows[int(rowRep)])

    # Look for instr that repeat like 'Rows 3 and 4:'

    # Loop over the rows and add in details for any missing rows; i.e. "and all other odd rows"
    try:
        if firstRowRepeatsOdd(rows[1]) and rowMissingInstr(rows[3]):
            # For now we're assuming if the word odd is in the first row instr, and some odd rows are missing instructions, to rep 1st row for odd
            for rownum, rowinstr in rows.items():
                if rownum != 1 and rownum % 2 != 0:
                    logging.debug(rows[1])
                    rows[rownum] = replaceRowWithNumInstr(rownum, rows[1])
                    logging.debug("m odd instr:")
                    logging.debug(rowinstr)
        elif secondRowRepeatsEven(rows[1]) and rowMissingInstr(rows[2]):
            # For now we're assuming if the word even is in the second row instr, and some even rows are missing instructions, to rep 2nd row for even
            for rownum, rowinstr in rows.items():
                if rownum > 2 and rownum % 2 == 0:
                    logging.debug(rows[2])
                    rows[rownum] = replaceRowWithNumInstr(rownum, rows[2])
                    logging.debug("m even instr:")
                    logging.debug(rowinstr)
    except:
        logging.error("Something went wrong")

    # Loop over the rows and add in any missing rows that are specified; i.e. "Rows 2,4,6:"

    # Print out the transformed pattern as a dict list
    pat = {}  # Create dict format
    patrows = rows.values()  # Get each of the rows into list format
    logging.debug(patrows)
    pat[rows[0]] = patrows[1:]  # make the name of the pattern the key to the dict and the list of rows the value
    # Print
    logging.info(pat)

    # Write the new pat back to a file
    txtfilenamenew = str(txtfilename).replace('.txt', 'new.txt')
    newpatfile = open(txtfilenamenew, 'w')
    newpatfile.writelines(str(pat))
    newpatfile.close()

    patfile.close()


def replaceRowWithNumInstr(rowNum, rowInstr):
    '''Return the new row instru to contain the rowNum given'''
    rowIdx = rowInstr.index(':')
    endNewRowInstr = rowInstr[rowIdx + 1:]
    logging.debug(endNewRowInstr)
    return "Row " + str(rowNum) + ":" + endNewRowInstr


def firstRowRepeatsOdd(rowOneInstr):
    '''Returns True if the first row instruction contains the word odd'''
    if "odd" in rowOneInstr:
        # Possibly a repeating odd row instruction
        logging.info("Possibly a repeating odd row instr:" + rowOneInstr)
        return True
    return False


def secondRowRepeatsEven(rowTwoInstr):
    '''Returns True if the first row instruction contains the word even'''
    if "even" in rowTwoInstr:
        # Possibly a repeating even row instruction
        logging.info("Possibly a repeating even row instr:" + rowTwoInstr)
        return True
    return False


def rowMissingInstr(row):
    '''Returns True if the only instr is the Row number'''
    rowpieces = row.split(' ')
    if len(rowpieces) == 3 and rowpieces[0] == "Row" and len(rowpieces[2]) == 0:
        logging.info("Missing instr for " + row)
        return True
    return False


def replaceRepRow(rowinstr, replaceWithRowInstr):
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
        rowToRep = rowWords[repIdx + 2]  # Adding 2 'cause it should be 'Rep', 'Row', '<row num we want>'
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
                rowNum = getRowNumFromInstr(rowinstr)
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


def getRowNumFromInstr(rowinstr):
    '''Return the row num in this instruction, or if mult are listed, the first one; i.e. Rows 2,4,6 would return 2; if not found returns -1'''
    rowNum = getNumFromNextWordAfterTerm(rowinstr, "Row")
    if rowNum == -1:
        rowNum = getNumFromNextWordAfterTerm(rowinstr, "Rows")

    return rowNum


def get_num_from_next_word_after_term(sentence, searchTerm):
    next_word = getNextWordAfterTerm(sentence, searchTerm, " ")
    if next_word:
        return get_numbers_from_str(next_word)
    return -1


def getNumFromNextWordAfterTerm(sentence, searchTerm):
    '''Get a number in the sentence following the word searchTerm; else return -1'''
    nextWord = getNextWordAfterTerm(sentence, searchTerm, " ")
    if nextWord:
        return getJustNumber(nextWord)
    return -1


def search_word_in_line(sentence, searchTerm):
    ''' returns index of searchTerm in sentence; else returns empty string '''
    # wordList = sentence.split(splitter)
    try:
        searchTermIdx = sentence.index(searchTerm)
    except ValueError:
        logging.warning("searchTerm:" + searchTerm + " was not found in sentence:" + sentence)
        return 0
    return searchTermIdx


def getNextWordAfterTerm(sentence, searchTerm, splitter):
    '''Splits sentence on splitter, then gives you the word after the searchTerm; returns empty string '''
    wordList = sentence.split(splitter)
    try:
        searchTermIdx = wordList.index(searchTerm)
    except ValueError:
        logging.warning("searchTerm:" + searchTerm + " was not found in sentence:" + sentence)
        return ''

    nextWordIdx = searchTermIdx + 1
    if nextWordIdx > len(wordList):
        logging.warning("searchTerm:" + searchTerm + " was the last word in sentence:" + sentence)
        return ''
    return wordList[nextWordIdx]  # Adding 1 'cause it should be 'Row', '<row num we want>:'


def getJustNumber(wordStrWNumber):
    '''Searches the wordStr for a number and strips out anything non-numeric; returns number as a string, or empty string if no number found'''
    return str(re.sub("[^0-9]", "", wordStrWNumber))


def get_numbers_from_str(word_str_w_numbers):
    '''Returns a list of numbers in the string'''
    repl_non_num_w_space = re.sub("[^0-9\-]", "", word_str_w_numbers.strip())
    nums = repl_non_num_w_space.split("-")
    return nums


def patt_writer(argv):
    filename = ''
    patt_type = ''
    try:
        opts, args = getopt.getopt(argv, "hf:p:b:", ["file=", "patt="])
    except getopt.GetoptError:
        print('patternUtil.py -f <file-name> -p <pattern-type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('patternUtil.py -f <file-name> -p <pattern-type>')
            sys.exit()
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-p", "--patt"):
            patt_type = arg.upper()
        elif opt in "-b":
            patt_type = ''

    if filename == '':
        logging.info("No filename of pattern given")
        return

    if patt_type == '':
        logging.info("Defaulting to patt type of Rounds")
        patt_type = 'ROUNDS'
    else:
        logging.info("Filename of pattern given:" + filename
                     )

    read_pattern_from_text(filename)


if __name__ == "__main__":
    patt_writer(sys.argv[1:])
