from unittest import TestCase

from src.knit_structure.enums.Side import Side
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.WrapDirection import WrapDirection


class TestWorkingYarn(TestCase):
    def test_init_default_working_yarn(self):
        # Test initializing WorkingYarn with default values, no args
        wy = WorkingYarn()

        self.assertEqual(wy.wrap_direction, WrapDirection.NORMAL)
        self.assertEqual(wy.num_wraps, 1)
        self.assertEqual(wy.yarn_action, None)

    def test_init_one_arg_unnamed_working_yarn(self):
        # Test initializing WorkingYarn with one unnamed arg
        wy = WorkingYarn(WrapDirection.TWISTED)

        self.assertEqual(wy.wrap_direction, WrapDirection.TWISTED)
        self.assertEqual(wy.num_wraps, 1)
        self.assertEqual(wy.yarn_action, None)

    def test_init_one_arg_named_none_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(_wrap_direction=WrapDirection.NONE)

        self.assertEqual(wy.wrap_direction, WrapDirection.NONE)
        self.assertEqual(wy.num_wraps, 0)
        self.assertEqual(wy.yarn_action, None)

    def test_init_one_arg_named_one_unnamed_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(WrapDirection.NONE, _yarn_action=Side.FRONT)

        self.assertEqual(wy.wrap_direction, WrapDirection.NONE)
        self.assertEqual(wy.num_wraps, 0)
        self.assertEqual(wy.yarn_action, Side.FRONT)

    def test_init_one_arg_named_normal_back_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(_wrap_direction=WrapDirection.NORMAL)

        self.assertEqual(wy.wrap_direction, WrapDirection.NORMAL)
        self.assertEqual(wy.num_wraps, 1)
        self.assertEqual(wy.yarn_action, None)

    def test_init_two_arg_named_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(_wrap_direction=WrapDirection.NORMAL, _num_wraps=2)

        self.assertEqual(wy.wrap_direction, WrapDirection.NORMAL)
        self.assertEqual(wy.num_wraps, 2)
        self.assertEqual(wy.yarn_action, None)

    def test_init_three_arg_named_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(_wrap_direction=WrapDirection.NORMAL, _num_wraps=2, _yarn_action=Side.FRONT)

        self.assertEqual(wy.wrap_direction, WrapDirection.NORMAL)
        self.assertEqual(wy.num_wraps, 2)
        self.assertEqual(wy.yarn_action, Side.FRONT)

    def test_init_three_arg_half_named_working_yarn(self):
        # Test initializing WorkingYarn with one named arg, and wrap direction None
        wy = WorkingYarn(WrapDirection.NORMAL, _num_wraps=2)

        self.assertEqual(wy.wrap_direction, WrapDirection.NORMAL)
        self.assertEqual(wy.num_wraps, 2)
        self.assertEqual(wy.yarn_action, None)

    # Test the str rep of WorkingYarn
    def test_str_rep_working_yarn(self):
        # Test what Working Yarn prints
        working_yarn = WorkingYarn(WrapDirection.NORMAL, _num_wraps=1)
        self.assertEqual(working_yarn.get_str_rep(), "")

        working_yarn = WorkingYarn(WrapDirection.NORMAL, _num_wraps=2)
        self.assertEqual(working_yarn.get_str_rep(), "wrapping yarn 2 times")

        working_yarn = WorkingYarn(WrapDirection.NORMAL, _num_wraps=3)
        self.assertEqual(working_yarn.get_str_rep(), "wrapping yarn 3 times")

        working_yarn = WorkingYarn(WrapDirection.TWISTED, _num_wraps=1)
        self.assertEqual(working_yarn.get_str_rep(), "wrapping yarn in a twisted, clockwise direction")

        working_yarn = WorkingYarn(WrapDirection.NONE, _num_wraps=0, _yarn_action=Side.FRONT)
        self.assertEqual(working_yarn.get_str_rep(), "with working yarn held in front")

        working_yarn = WorkingYarn(WrapDirection.NONE, _num_wraps=0, _yarn_action=Side.BACK)
        self.assertEqual(working_yarn.get_str_rep(), "with working yarn held in back")

        working_yarn = WorkingYarn(WrapDirection.NONE, _num_wraps=1, _yarn_action=Side.FRONT)
        self.assertEqual(working_yarn.get_str_rep(), "with working yarn held in front")
