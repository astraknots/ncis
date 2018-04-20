from unittest import TestCase
import astrology_signs as signs

class TestSigns(TestCase):
    def test_get_ordered_signs(self):
        self.assertEqual(signs.get_ordered_signs(0), signs.THE_SIGNS)
        self.assertEqual(signs.get_ordered_signs(1), list(signs.THE_SIGNS[1:]) + [signs.THE_SIGNS[0]])
        self.assertEqual(signs.get_ordered_signs(2), list(signs.THE_SIGNS[2:]) + list(signs.THE_SIGNS[0:2]))
        self.assertEqual(signs.get_ordered_signs(3), list(signs.THE_SIGNS[3:]) + list(signs.THE_SIGNS[0:3]))
        self.assertEqual(signs.get_ordered_signs(4), list(signs.THE_SIGNS[4:]) + list(signs.THE_SIGNS[0:4]))
        self.assertEqual(signs.get_ordered_signs(5), list(signs.THE_SIGNS[5:]) + list(signs.THE_SIGNS[0:5]))
        self.assertEqual(signs.get_ordered_signs(6), list(signs.THE_SIGNS[6:]) + list(signs.THE_SIGNS[0:6]))
        self.assertEqual(signs.get_ordered_signs(7), list(signs.THE_SIGNS[7:]) + list(signs.THE_SIGNS[0:7]))
        self.assertEqual(signs.get_ordered_signs(8), list(signs.THE_SIGNS[8:]) + list(signs.THE_SIGNS[0:8]))
        self.assertEqual(signs.get_ordered_signs(9), list(signs.THE_SIGNS[9:]) + list(signs.THE_SIGNS[0:9]))
        self.assertEqual(signs.get_ordered_signs(10), list(signs.THE_SIGNS[10:]) + list(signs.THE_SIGNS[0:10]))
        self.assertEqual(signs.get_ordered_signs(11), list(signs.THE_SIGNS[11:]) + list(signs.THE_SIGNS[0:11]))

