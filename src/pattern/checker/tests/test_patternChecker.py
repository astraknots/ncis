from unittest import TestCase

from src.pattern.checker import patternChecker as pc

class TestPatternChecker(TestCase):
    def test_simplePatternStr(self):
        self.assertEqual(pc.parse_patt_str("(sl 1 st to cable needle and hold in front, k2, k1 from cable needle) twice"), ['sl 1 st to cable needle and hold in front', 'k2', 'k1 from cable needle', 'sl 1 st to cable needle and hold in front', 'k2', 'k1 from cable needle'])

    def test_countSts(self):
        self.assertEqual(pc.count_sts(['k1']), 1)

    def test_countInstrSts(self):
        self.assertEqual(pc.count_instr_sts('k1'), 1)
#    st_cnt = count_sts(parsed_instr, specials)

