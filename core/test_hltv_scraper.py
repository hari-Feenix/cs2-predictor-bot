import unittest
from core.hltv_scraper import get_upcoming_matches

class TestHLTVScraper(unittest.TestCase):
    def test_get_upcoming_matches_returns_list(self):
        result = get_upcoming_matches()
        self.assertIsInstance(result, list)
        if result:  # Only check if list is not empty
            self.assertIn('team1', result[0])
            self.assertIn('team2', result[0])
            self.assertIn('time', result[0])

if __name__ == '__main__':
    unittest.main()
