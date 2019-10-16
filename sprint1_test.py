import unittest
from datetime import datetime
from project_03 import Person, Family, Classification
from project_03 import valid_date

classify = Classification('/Users/nadik/Desktop/gedcom-analyzer/us01_us03.ged')

class StoryTest(unittest.TestCase):

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

    def test_us04(self):
        """Function that tests us04_marriage_before_divorse()"""
        marriage_divorse = classify.us04_marriage_before_divorse()
        expect = 'ERROR: FAMILY: US04: (line# goes here) @F4@: Divorced 13 DEC 2005 before married on 14 JUL 2006'
        self.assertEqual(marriage_divorse, expect)

    def test_us27(self):
        """Function that tests us27_individual_ages()"""
        individual_ages = list(classify.us27_individual_ages())
        expect =  [('@I3@', 71), ('@I4@', 0), ('@I5@', 0), ('@I6@', 38), ('@I7@', 35), ('@I8@', 22), ('@I9@', 23),
                    ('@I10@', 39), ('@I11@', 2), ('@I12@', 36), ('@I13@', 7), ('@I14@', 9), ('@I15@', 4),
                    ('@I16@', 42), ('@I17@', 6), ('@I18@', 3), ('@I19@', 4), ('@I20@', 28), ('@I21@', 1),
                    ('@I23@', 1), ('@I24@', 39), ('@I25@', 34), ('@I26@', 0), ('@I27@', 39), ('@28@', 68), 
                    ('@29@', 68), ('@30@', 39),]
        self.assertEqual (individual_ages, expect)

    def test_us31(self):
        """Function that tests us31_living_singles()"""
        #classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        living_singles_list = classify.us31_living_singles()
        expect =  [('@28@', 'Smith /Joseph'), ('@29@', 'Sasquatch /Kyle'), ('@30@', 'Birch /Cynthia')]
        self.assertEqual (living_singles_list, expect)
    
    def test_us32(self):
        """Function that tests us31_multiple_births()"""
        #classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        multiple_births = classify.us32_multiple_births()
        expect = {'6 NOV 1950': ['Smith /Joseph', 'Sasquatch /Kyle'], '6 NOV 1979': ['Lamar /Odom/', 'Birch /Cynthia']}
        self.assertEqual (multiple_births, expect)

    def test_us35(self):
        """Function that tests us35_recent_births()"""
        #classify = Classification('us35_us42.ged')
        recent_births = classify.us35_recent_births()
        expect =  {'17 SEP 2019': ['Rob /Kardashian/'], '18 SEP 2019': ['Kourtney /Kardashian/']}
        self.assertEqual (recent_births, expect)
    
    def test_valid_date(self):
        """Function that tests valid_date()"""
        self.assertEqual (valid_date('10 SEP 2019'), True)
        self.assertEqual (valid_date('31 FRB 2019'), False)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
