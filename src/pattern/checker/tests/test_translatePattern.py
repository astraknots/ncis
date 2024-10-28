from unittest import TestCase

from src.pattern.translatePattern import consolidate_list_to_single_instr, convert_to_repeat


class Test(TestCase):
    def test_consolidate_list_to_single_instr(self):
        self.assertEqual(consolidate_list_to_single_instr(['k1']), 'k1')
        self.assertEqual(consolidate_list_to_single_instr(['']), '')
        self.assertEqual(consolidate_list_to_single_instr([]), '')
        self.assertEqual(consolidate_list_to_single_instr(['k1', 'k1']), "k1, k1")
        self.assertEqual(consolidate_list_to_single_instr(['k1', 'k1'], " | "), "k1 | k1")
        self.assertEqual(consolidate_list_to_single_instr(['k1', 'k1'], " "), "k1 k1")
        self.assertEqual(consolidate_list_to_single_instr(['k1', 'k1', 'p2']), "k1, k1, p2")


class Test(TestCase):
    def test_convert_to_repeat(self):
        self.assertEqual(convert_to_repeat(['k1', 'p1'], num_reps=2, rep_phrase='times'), ['(k1, p1) 2 times'])
        self.assertEqual(convert_to_repeat(['k2', 'k2'], rep_phrase='twice'), ['(k2, k2) twice'])
        self.assertEqual(convert_to_repeat(['k2', 'k2tog'], rep_phrase='twice'), ['(k2, k2tog) twice'])
        self.assertEqual(convert_to_repeat(['k2', 'k2tog'], delim=', ', rep_ind_l='*(', rep_ind_r=')*', rep_phrase='rep from * to * to end'),
                         ['*(k2, k2tog)* rep from * to * to end'])
        self.assertEqual(convert_to_repeat(['k2', 'k2tog'], delim=', ', rep_ind_l='*', rep_ind_r='*', rep_phrase='rep from * to * to end'),
                         ['*k2, k2tog* rep from * to * to end'])