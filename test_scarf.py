import unittest, scarf

class TestScarfMethods(unittest.TestCase):

    def test_replaceRepStr(self):
        self.assertEqual(scarf.replace_rep_str("K the pattern, rep from *", 5), "K the pattern, rep from * (5) times")

    def test_getLargest(self):
        self.assertEqual(scarf.get_largest([1, 2, 3]), 3)

    def test_rectifyDegreeByAsc(self):
        self.assertEqual(scarf.rectify_degree_by_asc(1, 100), 99)
        self.assertEqual(scarf.rectify_degree_by_asc(100, 1), 261)
        self.assertEqual(scarf.rectify_degree_by_asc(360, 1), 1)
        # check that scarf.rectifyDegreeByAsc fails when diff of degree values (args) are greater than 360
        with self.assertRaises(ValueError):
            scarf.rectify_degree_by_asc(1, 364)
            scarf.rectify_degree_by_asc(365, 364)



if __name__ == '__main__':
    unittest.main()