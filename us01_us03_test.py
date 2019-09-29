import unittest
from datetime import datetime
from datetime import date
from project_03 import Person, Family, Classification

classify = Classification('/Users/MaramAlrshoud/Documents/Universites/Stevens/Fall 2019/SSW 555/Week5/us01_us04.ged')

class StoriesTest(unittest.TestCase):

    def test_us01(self):
        'US01 test Dates (birth, marriage, divorce, death) should not be after the current date'

        day = '24 Sep 2019'
        d1= datetime.strptime(day, '%d %b %Y')
        us01= classify.us01_before_current_dates(d1)
        expect = ['INDI BIRTH ERROR', 'INDI DEAT ERROR', 'FAM MARR ERROR', 'FAM DIVO ERROR']   

        self.assertEqual(us01, expect)

    
    def test_us03(self):
        'US03 test Birth should occur before death of an individual'
        
        us03 = classify.us03_birth_before_death()
        expect = 'ERROR: INDIVIDUAL: US03: LINE NUMBER: @I2@ : Died 30 SEP 1943 before born 22 FEB 1944'

        self.assertEqual(us03,expect)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)