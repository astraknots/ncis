
from unittest import TestCase
import chartWriter as cw


class TestChartWriter(TestCase):
    def test_inc_cnt_to_next_sign(self):
        # Test that degree increments will increment to the next sign after 30 degrees
        for deginc in range(1, 13):
            cnt_true = 0
            with self.subTest(deginc=deginc):
                for x_d in range(0, 360, deginc): # loop over all 360 degrees
                    cnt_true += cw.inc_cnt_to_next_sign(x_d, deginc)

                self.assertEqual(cnt_true, 11)  # sign should have changed 12 times




