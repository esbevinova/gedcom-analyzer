import unittest
from project_03 import Person, Family, Classification
from project_03 import valid_tag

class CommonTest(unittest.TestCase):

    def test_us31(self):
        classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        living_singles_list = classify.us31_living_singles()
        expect =  [('@28@', 'Smith /Joseph'), ('@29@', 'Sasquatch /Kyle'), ('@30@', 'Birch /Cynthia')]
        self.assertEqual (living_singles_list, expect)
    
    def test_us32(self):
        classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        multiple_births = classify.us32_multiple_births()
        expect = {'6 NOV 1950': ['Smith /Joseph', 'Sasquatch /Kyle'], '6 NOV 1979': ['Lamar /Odom/', 'Birch /Cynthia']}
        self.assertEqual (multiple_births, expect)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)