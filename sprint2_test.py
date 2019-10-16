import unittest
from datetime import datetime
from project_03 import Person, Family, Classification
from project_03 import valid_date

classify = Classification('./test_results.ged')


class StoryTest(unittest.TestCase):

    def test_us01(self):
        'US01 test Dates (birth, marriage, divorce, death) should not be after the current date'

        day = '24 Sep 2019'
        d1= datetime.strptime(day, '%d %b %Y')
        us01= classify.us01_before_current_dates(d1)
        expect = ['INDI BIRTH ERROR', 'INDI DEAT ERROR', 'FAM MARR ERROR', 'FAM DIVO ERROR']   

        self.assertEqual(us01, expect)
    
    def test_us02(self):
        'Function that tests us02_death_before_marriage(): US02 Birth should occur before marriage of an individual'      
        us02 = list(classify.us02_death_before_marriage())
        expect = ["ERROR: FAMILY: US02: ID: @I1@ - Wife's birth date 2020-11-05 on line 22 occurs after her marriage date 1978-07-08 on line 347",
                  "ERROR: FAMILY: US02: ID: @I1@ - Wife's birth date 2020-11-05 on line 22 occurs after her marriage date 2020-04-24 on line 357",
                  "ERROR: FAMILY: US02: ID: @I4@ - Husband's birth date 2019-09-17 on line 53 occurs after his marriage date 2016-08-11 on line 366",
                  "ERROR: FAMILY: US02: ID: @I5@ - Wife's birth date 2019-09-18 on line 63 occurs after her marriage date 2006-07-14 on line 377"]
        self.assertEqual(us02,expect)
       
    def test_us03(self):
        'US03 test Birth should occur before death of an individual'
        
        us03 = list(classify.us03_birth_before_death())
        expect = ['ERROR: INDIVIDUAL: US03: @I2@: Died on 30 SEP 1943: line (34): before born on 22 FEB 1944']

        self.assertEqual(us03,expect)

    def test_us04(self):
        """Function that tests us04_marriage_before_divorse()"""
        marriage_divorse = list(classify.us04_marriage_before_divorse())
        expect = ['ERROR: FAMILY: US04: @F4@: Divorced on 13 DEC 2005 (line 379) before married on 14 JUL 2006 (line 377)']
        print(marriage_divorse)
        self.assertEqual(marriage_divorse, expect)
        
    def test_us05(self):
        """Function that tests us05_marriage_before_death()"""
        marriage = list(classify.us05_marriage_before_death())
        expect =["ERROR: FAMILY: US05: @F1@: Married on 1978-07-08 (line 347) after Death of Husband on 1943-09-30 (line 34)","ERROR: FAMILY: US05: @F13@: Married on 2019-07-08 (line 446) after Death of Wife on 2000-06-12 (line 319)"]
        print(marriage)
        self.assertEqual(marriage, expect)

    def test_us06(self):
        """Function that tests us06_divorce_before_death()"""
        divorse = list(classify.us06_divorce_before_death())
        expect = ["ERROR: FAMILY: US06: @F2@: Divorced on 2021-03-23 (line 359) after Death of Husband on 2020-11-30 (line 44)","ERROR: FAMILY: US06: @F12@: Divorced on 2016-03-10 (line 438) after Death of Wife on 2000-09-30 (line 298)"]
        print(divorse)
        self.assertEqual(divorse, expect)

    def test_us07(self):
        """Function tests us07_over150()"""
        us07 = list(classify.us07_over150())
        print(us07)
        expect = ['ERROR: INDIVIDUAL: US07: @31@ More than 150 years old: Birthday 16 DEC 1770 (line 281)', 
                'ERROR: INDIVIDUAL: US07: @32@ More than 150 years old at death: Birthday 31 MAR 1685 (line 286), Death date 31 MAR 1887 (line 288)']          
        self.assertEqual(us07, expect)
    
    def test_us10(self):
        """Function that tests us10_marriage_after14() US10: parents must be at least 14 years old at the time of marriage""" 
        us10 = list(classify.us10_marriage_after14())
        expect = ["ERROR: FAMILY: US10: ID: @F1@: wife's age is less than 14 years old at the time of marriage 8 JUL 1978 (line 347)",
                  "ERROR: FAMILY: US10: ID: @F2@: wife's age is less than 14 years old at the time of marriage 24 APR 2020 (line 357)",
                  "ERROR: FAMILY: US10: ID: @F3@: husband's age is less than 14 years old at the time of marriage 11 AUG 2016 (line 366)",
                  "ERROR: FAMILY: US10: ID: @F4@: wife's age is less than 14 years old at the time of marriage 14 JUL 2006 (line 377)"]
        self.assertEqual(us10, expect)

    def test_us27(self):
        """Function that tests us27_individual_ages()"""
        individual_ages = list(classify.us27_individual_ages())
        expect =  [('@I3@', 71), ('@I4@', 0), ('@I5@', 0), ('@I6@', 38), ('@I7@', 35), ('@I8@', 22), ('@I9@', 23),
                    ('@I10@', 39), ('@I11@', 2), ('@I12@', 36), ('@I13@', 7), ('@I14@', 9), ('@I15@', 4),
                    ('@I16@', 42), ('@I17@', 6), ('@I18@', 3), ('@I19@', 4), ('@I20@', 28), ('@I21@', 1),
                    ('@I23@', 1), ('@I24@', 39), ('@I25@', 34), ('@I26@', 0), ('@I27@', 39), ('@28@', 68), 
                    ('@29@', 68), ('@30@', 39), ('@31@', 248), ('@32@', 202)]
        self.assertEqual (individual_ages, expect)
    
    def test_us29_list_deceased(self):
        'US29 test deceased individual'

        us29 = classify.us29_list_deceased()
        expect = [('Robert /Kardashian/', '30 SEP 1943'), ('Johann /Bach', '31 MAR 1887'), ('Jeny /Jenner/', '30 SEP 2000'), ('Yan /Jenner/', '12 JUN 2000')]
        self.assertEqual (us29, expect)

    def test_us30_list_living_married(self):
        'US30 test living_married'
        
        us30 = classify.us30_list_living_married()
        expect = [('@I1@', 'Kris /Jenner/'), ('@I6@', 'Kim /Kardashian/'),
                  ('@I16@', 'Kaney /West/'), ('@I8@', 'Kylie /Jenner/'), ('@I22@', 'Travis /Scott/')]
 
        self.assertEqual (us30,expect)

    def test_us31(self):
        """Function that tests us31_living_singles()"""
        #classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        living_singles_list = classify.us31_living_singles()
        expect =  [('@28@', 'Smith /Joseph'), ('@29@', 'Sasquatch /Kyle'), ('@30@', 'Birch /Cynthia'), ('@31@', 'Ludwig /Beethoven'), ('@I36@', 'Chris /Kardashian/')]
        self.assertEqual (living_singles_list, expect)
    
    def test_us32(self):
        """Function that tests multiple_births()"""
        #classify = Classification('/Users/katya/Documents/Fall19/555/revised_gedcom/us31_us32.ged')
        multiple_births = classify.us32_multiple_births()
        expect = {'22 FEB 1944': ['Robert /Kardashian/', 'George /Kardashian/'], '6 NOV 1979': ['Lamar /Odom/', 'Birch /Cynthia'], '6 NOV 1950': ['Smith /Joseph', 'Sasquatch /Kyle'], '5 NOV 1950': ['Jeny /Jenner/', 'Yan /Jenner/']}
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
        self.assertEqual (valid_date('31 FRB 2019'), None)



if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
