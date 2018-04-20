from unittest import TestCase

import patternUtil as pu


class TestPatternUtil(TestCase):
    def test_get_row_num_from_instr(self):
        self.assertEqual(pu.get_row_num_from_instr("Row 1:"), '1')
        self.assertEqual(pu.get_row_num_from_instr("Row 1 :"), '1')
        self.assertEqual(pu.get_row_num_from_instr("Rows 2, 4, 6:"), '2')
        self.assertEqual(pu.get_row_num_from_instr("sdflksjdf"), -1)

    def test_get_next_word_after_term(self):
        self.assertEqual(pu.get_next_word_after_term("Row 1 (WS) and all other odd rows: Purl", "Row", " "), '1')
        self.assertEqual(pu.get_next_word_after_term("Row 2: *LT, (RT) twice; rep from *, end LT, RT", "Row", " "), '2:')
        self.assertEqual(pu.get_next_word_after_term("Rows 7 and 9: K", "Row", " "), '')
        self.assertEqual(pu.get_next_word_after_term("Rows 7 and 9: K", "Rows", " "), '7')
        self.assertEqual(pu.get_next_word_after_term("Row 4: *K2tog, K1*, rep from *", "*", " "), '')
        '''with self.assertRaises(ValueError):
            pu.getNextWordAfterTerm("Rows 7 and 9: K", "Row", " ")'''

    def test_get_num_from_next_word_after_term(self):
        self.assertEqual(pu.get_num_from_next_word_after_term("Row 1 (WS) and all other odd rows: Purl", "Row"), "1")
        self.assertEqual(pu.get_num_from_next_word_after_term("Row 2: *LT, (RT) twice; rep from *, end LT, RT", "Row"), "2")
        self.assertEqual(pu.get_num_from_next_word_after_term("Rows 7 and 9: K", "Rows"), "7")
        self.assertEqual(pu.get_num_from_next_word_after_term("Rows 7 and 9: K", "K"), -1)

    def test_get_just_number(self):
        self.assertEqual(pu.get_just_number("1:"), "1")
        self.assertEqual(pu.get_just_number("2"), "2")
        self.assertEqual(pu.get_just_number("3 "), "3")
        self.assertEqual(pu.get_just_number(" 4 "), "4")
        self.assertEqual(pu.get_just_number("w5"), "5")
        self.assertEqual(pu.get_just_number("wjkl"), "")
