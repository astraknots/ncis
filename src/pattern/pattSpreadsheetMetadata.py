
'''
A pattern in spreadsheet is assumed to have the following structure and attributes:
Cell A1 contains whether this is a pattern in 'ROW's or 'ROUND's --> RowsOrRnds.get_from_str (captured in: PATT_WORKED)
The First column of the spreadsheet (cells A2:An) contains numbered rows or rounds ASC (total value captured in: PATT_NUM_ROWS)
The First row of the spreadsheet (cells A1:Zn) contain numbered stitches (total value captured in: PATT_ST_CNT)
The cells B2:Zn contain individual stitch instruction (i.e. k, k2tog, yo, or are blank (read in as 'nan') to indicate no stitch
Unlike typical knitting charts, the pattern is read from top down and left to right
'''

# These values will be interpretted from what the spreadsheet contains
# These values speak to the pattern overall, and are stored in the top level of the Pattern Dictionary
PATT_ST_CNT = "Pattern St Cnt:"
''' Contains an int value of total stitches this pattern spreadsheet defined'''

PATT_NUM_ROWS = "Pattern Row Cnt:"  # TODO: for now, we'll call them all rows
''' Contains an int value of total number of rows/rnds this pattern spreadsheet defined'''

PATT_WORKED = "Worked Flat (in Rows) or in the Round"
''' Contains an RowsOrRounds enum representing how this pattern spreadsheet defined how this pattern is worked'''

PATT_INSTRS = "Pattern Instructions:"
''' Contains a dictionary of Pattern instructions by row/rnd ex: key: 'Row 1:', value: [<list of str patt instrs for row>] '''

PATT_ROW_ENDING_ST_CNT = "sts ending"
''' How many sts remain after this row has been worked 
Contains a dictionary of Row metadata with the same keys as PATT_INSTRS and corresponding to those rows. ex. {'Row 1:' : 41}'''

PATT_ROW_ENDING_ST_CHANGE_CNT = "sts inc or dec"
''' How many sts were increased or decreased
Contains a dictionary of Row metadata with the same keys as PATT_INSTRS and corresponding to those rows. ex. {'Row 1:' : 2}'''

PATT_ROW_SHAPING = "inc or dec"
''' Whether the row resulted in an increase or decrease: IncOrDec enum
Contains a dictionary of Row metadata with the same keys as PATT_INSTRS and corresponding to those rows. ex. {'Row 1:' : IncOrDec.INC}'''