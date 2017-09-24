import unittest, scarf

class TestScarfMethods(unittest.TestCase):

    def test_replaceRepStr(self):
        self.assertEqual(scarf.replaceRepStr("K the pattern, rep from *", 5), "K the pattern, rep from * (5) times")

    def test_getLargest(self):
        self.assertEqual(scarf.getLargest([1,2,3]), 3)

    def test_rectifyDegreeByAsc(self):
        self.assertEqual(scarf.rectifyDegreeByAsc(1, 100), 99)
        self.assertEqual(scarf.rectifyDegreeByAsc(100, 1), 261)
        self.assertEqual(scarf.rectifyDegreeByAsc(360, 1), 1)
        # check that scarf.rectifyDegreeByAsc fails when diff of degree values (args) are greater than 360
        with self.assertRaises(ValueError):
            scarf.rectifyDegreeByAsc(1, 364)
            scarf.rectifyDegreeByAsc(365, 364)



if __name__ == '__main__':
    unittest.main()