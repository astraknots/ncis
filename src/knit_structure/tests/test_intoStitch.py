from unittest import TestCase

from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.enums.StitchPart import StitchPart


class TestIntoStitch(TestCase):
    def test_init_default_into_stitch(self):
        # Test initializing IntoStitch with default values, no args
        into_st = IntoStitch()

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 1)
        self.assertEqual(into_st.num_rows_below, 0)

    def test_init_back_part_into_stitch(self):
        # Test initializing IntoStitch with 1 provided value
        into_st = IntoStitch(StitchPart.BACK)

        self.assertEqual(into_st.into_st, StitchPart.BACK)
        self.assertEqual(into_st.num_worked_into, 1)
        self.assertEqual(into_st.num_rows_below, 0)

    def test_init_two_args_into_stitch(self):
        # Test initializing IntoStitch with 2 provided values
        into_st = IntoStitch(StitchPart.FRONT, 2)

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 0)

    def test_init_three_args_into_stitch(self):
        # Test initializing IntoStitch with 3 provided values
        into_st = IntoStitch(StitchPart.FRONT, 2, 1)

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 1)

    def test_init_rows_below_named_into_stitch(self):
        # Test initializing IntoStitch with 1 unnamed, and 1 named value
        into_st = IntoStitch(StitchPart.FRONT, num_rows_below=2)

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 1)
        self.assertEqual(into_st.num_rows_below, 2)

    def test_init_num_worked_named_into_stitch(self):
        # Test initializing IntoStitch with 1 unnamed, and 1 named value
        into_st = IntoStitch(StitchPart.FRONT, num_worked_into=2)

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 0)

    def test_init_named_diff_order_into_stitch(self):
        # Test initializing IntoStitch with diff ordered, named ars
        into_st = IntoStitch(num_worked_into=2, into_st=StitchPart.BACK)

        self.assertEqual(into_st.into_st, StitchPart.BACK)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 0)

    def test_init_named_diff_order2_into_stitch(self):
        # Test initializing IntoStitch with diff ordered, named ars
        into_st = IntoStitch(num_rows_below=1, num_worked_into=2)

        self.assertEqual(into_st.into_st, StitchPart.FRONT)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 1)

    def test_init_unnamed_back_into_stitch(self):
        # Test initializing IntoStitch with 1 unnamed, and 1 named value
        into_st = IntoStitch(StitchPart.BACK, num_worked_into=2)

        self.assertEqual(into_st.into_st, StitchPart.BACK)
        self.assertEqual(into_st.num_worked_into, 2)
        self.assertEqual(into_st.num_rows_below, 0)

    # Test the str rep of Into Stitch
    def test_str_rep_into_stitch(self):
        # Test what Into Stitch prints
        into_st = IntoStitch(StitchPart.BACK, num_worked_into=2)
        self.assertEqual(into_st.get_str_rep(), "into back of 2 stitches")

        into_st = IntoStitch(StitchPart.FRONT, num_worked_into=1)
        self.assertEqual(into_st.get_str_rep(), "into front of 1 stitch")

        into_st = IntoStitch(StitchPart.FRONT, num_worked_into=0)
        self.assertEqual(into_st.get_str_rep(), "")

        into_st = IntoStitch(StitchPart.FRONT, num_worked_into=2)
        self.assertEqual(into_st.get_str_rep(), "into front of 2 stitches")

        into_st = IntoStitch(StitchPart.BELOW_L, num_rows_below=2)
        self.assertEqual(into_st.get_str_rep(), "into st below st on LHN of stitch 2 rows below")

        into_st = IntoStitch(StitchPart.BELOW_R, num_rows_below=1)
        self.assertEqual(into_st.get_str_rep(), "into st below st on RHN of stitch 1 rows below")

        into_st = IntoStitch(StitchPart.BACK, num_rows_below=0, num_worked_into=2)
        self.assertEqual(into_st.get_str_rep(), "into back of 2 stitches")

        into_st = IntoStitch(StitchPart.BAR, num_rows_below=0, num_worked_into=1)
        self.assertEqual(into_st.get_str_rep(), "into the bar between stitches on the needle")
