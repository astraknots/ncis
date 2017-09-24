#!/usr/bin/python

import logging, re
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def convertPatternFromWeb(txtfilename):
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
            rows[rownum] = replaceRepRow(rowinstr, rows[int(rowRep)])


    #Look for instr that repeat like 'Rows 3 and 4:'


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


def replaceRowWithNumInstr(rowNum, rowInstr):
    '''Return the new row instru to contain the rowNum given'''
    rowIdx = rowInstr.index(':')
    endNewRowInstr = rowInstr[rowIdx+1:]
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


def getNumFromNextWordAfterTerm(sentence, searchTerm):
    '''Get a number in the sentence following the word searchTerm; else return -1'''
    nextWord = getNextWordAfterTerm(sentence, searchTerm, " ")
    if nextWord:
        return getJustNumber(nextWord)
    return -1


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