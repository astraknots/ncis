from unittest import TestCase
import signs


class TestSigns(TestCase):
    def test_getFirstHouseSignIdx(self):
        # Test if the sign isnt in the const, we raise exception
        with self.assertRaises(ValueError):
            signs.getHouseSignIdx('FOO')

        # Test valid sign placements, these are 0 indexed
        self.assertEqual(signs.getHouseSignIdx('ARIES'), 0)
        self.assertEqual(signs.getHouseSignIdx('TAURUS'), 1)
        self.assertEqual(signs.getHouseSignIdx('GEMINI'), 2)
        self.assertEqual(signs.getHouseSignIdx('CANCER'), 3)
        self.assertEqual(signs.getHouseSignIdx('LEO'), 4)
        self.assertEqual(signs.getHouseSignIdx('VIRGO'), 5)
        self.assertEqual(signs.getHouseSignIdx('LIBRA'), 6)
        self.assertEqual(signs.getHouseSignIdx('SCORPIO'), 7)
        self.assertEqual(signs.getHouseSignIdx('SAGITARRIUS'), 8)
        self.assertEqual(signs.getHouseSignIdx('CAPRICORN'), 9)
        self.assertEqual(signs.getHouseSignIdx('AQUARIUS'), 10)
        self.assertEqual(signs.getHouseSignIdx('PISCES'), 11)



