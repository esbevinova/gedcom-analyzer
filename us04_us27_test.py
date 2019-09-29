import unittest
from project_03 import Person, Family, Classification

classify = Classification('/Users/nadik/Desktop/gedcom-analyzer/us04_us27.get')

class StoryTest(unittest.TestCase):

    def test_us04(self):
        """Function that tests us04_marriage_before_divorse()"""
        marriage_divorse = classify.us04_marriage_before_divorse()
        expect = 'ERROR: FAMILY: US04: (line# goes here) @F2@: Divorced 23 MAR 1990 before married on 12 APR 1991'
        self.assertEqual(marriage_divorse, expect)

    def test_us27(self):
        """Function that tests us27_individual_ages()"""
        individual_ages = list(classify.us27_individual_ages())
        expect =  [('@I1@', 63), ('@I2@', 59), ('@I3@', 69), ('@I4@', 32), ('@I5@', 40), ('@I10@', 39), ('@I12@', 36)]
        self.assertEqual (individual_ages, expect)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)