import unittest
from project_03 import Person, Family, Classification
from project_03 import valid_date

class CommonTest(unittest.TestCase):

    def test_us35(self):
        """Function that tests us35_recent_births()"""
        classify = Classification('us35_us42.ged')
        recent_births = classify.us35_recent_births()
        expect =  {'17 SEP 2019': ['Rob /Kardashian/'], '18 SEP 2019': ['Kourtney /Kardashian/']}
        self.assertEqual (recent_births, expect)
    
    
    def test_valid_date(self):
        """Function that tests valid_date()"""
        self.assertEqual (valid_date('10 SEP 2019'), True)
        self.assertEqual (valid_date('31 FRB 2019'), None)

    
if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)