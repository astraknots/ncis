from unittest import TestCase

import patternUtil as pu

class TestPatternUtil(TestCase):
    def test_getRowNumFromInstr(self):
        self.assertEqual(pu.getRowNumFromInstr("Row 1:"), '1')
        self.assertEqual(pu.getRowNumFromInstr("Row 1 :"), '1')
        self.assertEqual(pu.getRowNumFromInstr("Rows 2, 4, 6:"), '2')


    def test_getNextWordAfterTerm(self):
        self.assertEqual(pu.getNextWordAfterTerm("Row 1 (WS) and all other odd rows: Purl", "Row", " "), '1')
        self.assertEqual(pu.getNextWordAfterTerm("Row 2: *LT, (RT) twice; rep from *, end LT, RT", "Row", " "), '2:')
        self.assertEqual(pu.getNextWordAfterTerm("Rows 7 and 9: K", "Row", " "), '')
        self.assertEqual(pu.getNextWordAfterTerm("Rows 7 and 9: K", "Rows", " "), '7')
        '''with self.assertRaises(ValueError):
            pu.getNextWordAfterTerm("Rows 7 and 9: K", "Row", " ")'''


    def test_getNumFromNextWordAfterTerm(self):
        self.assertEqual(pu.getNumFromNextWordAfterTerm("Row 1 (WS) and all other odd rows: Purl", "Row"), "1")
        self.assertEqual(pu.getNumFromNextWordAfterTerm("Row 2: *LT, (RT) twice; rep from *, end LT, RT", "Row"), "2")
        self.assertEqual(pu.getNumFromNextWordAfterTerm("Rows 7 and 9: K", "Rows"), "7")


    def test_getJustNumber(self):
        self.assertEqual(pu.getJustNumber("1:"), "1")
        self.assertEqual(pu.getJustNumber("2"), "2")
        self.assertEqual(pu.getJustNumber("3 "), "3")
        self.assertEqual(pu.getJustNumber(" 4 "), "4")
        self.assertEqual(pu.getJustNumber("w5"), "5")
        self.assertEqual(pu.getJustNumber("wjkl"), "")
