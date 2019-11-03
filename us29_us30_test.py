import unittest
from datetime import datetime
from project_03 import Person, Family, Classification
from project_03 import valid_date

classify = Classification('/Users/MaramAlrshoud/Documents/Universites/Stevens/Fall 2019/SSW 555/Week6/gedcom-analyzer-Sprint2/test_results.ged')

class StoriesTest(unittest.TestCase):

    def test_us29_list_deceased(self):
        'US29 test deceased individual'

        us29 = classify.us29_list_deceased()
        expect = [('Robert /Kardashian/', '30 SEP 1943'), ('Johann /Bach', '31 MAR 1887')]
        self.assertEqual (us29, expect)

    def test_us30_list_living_married(self):
        'US30 test living_married'
        
        us30 = classify.us30_list_living_married()
        expect = [('@I1@', 'Kris /Jenner/'), ('@I6@', 'Kim /Kardashian/'),
                  ('@I16@', 'Kaney /West/'), ('@I8@', 'Kylie /Jenner/'), ('@I22@', 'Travis /Scott/')]
 
        self.assertEqual (us30,expect)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)