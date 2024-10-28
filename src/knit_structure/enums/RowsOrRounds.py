from enum import Enum


class RowsOrRounds(Enum):
    ROWS = 'rows'
    ROUNDS = 'rounds'
    NONE = ''
    ROW = 'Row'
    RND = 'Rnd'
    ROUND = 'ROUND'

    @staticmethod
    def from_str(row_rnd_str):
        row_rnd_str = row_rnd_str.upper()
        if row_rnd_str in ('ROW'):
            return RowsOrRounds.ROW
        elif row_rnd_str in ('ROWS'):
            return RowsOrRounds.ROWS
        elif row_rnd_str in ('ROUND'):
            return RowsOrRounds.ROUND
        elif row_rnd_str in ('ROUNDS', 'RNDS'):
            return RowsOrRounds.ROUNDS
        elif row_rnd_str in ('RND'):
            return RowsOrRounds.RND
        else:
            return RowsOrRounds.NONE
            # raise NotImplementedError
