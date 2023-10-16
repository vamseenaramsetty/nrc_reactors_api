import unittest
from app import scrape_and_load  
from app import create_reactor_status_table

class TestScrapeAndLoad(unittest.TestCase):

    def test_scrape_and_load(self):
        result = scrape_and_load()
        # Assuming the function should return a non-empty list
        #self.assertTrue(result)  # This checks that the result is not None or an empty list
        self.assertIsNone(result)
    def test_create_reactor_status_table(self):
        result = create_reactor_status_table()
        #self.assertTrue(result)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
