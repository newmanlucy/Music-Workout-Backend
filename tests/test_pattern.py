import unittest
from util import client_log

from client import post_pattern, get_patterns, delete_pattern

class TestUser(unittest.TestCase):


    # Test posting patterns

    def test_post_pattern_no_pattern(self):
        r = post_pattern(None)
        self.assertEqual(r.status_code, 400)

    def test_post_pattern_success(self):
        pattern = [1,2,3]
        r = post_pattern(pattern)
        self.assertEqual(r.status_code, 200)


    # Test getting patterns

    def test_get_pattern_succes(self):
        user = 

    
    # Test deleting patterns

    def test_delete_pattern_not_in_database(self):
        very_high_number = 10000000
        r = delete_pattern(very_high_number)
        self.assertEqual(r.status_code, 404)

    def test_delete_pattern_success(self):
        pass


if __name__ == '__main__':
    unittest.main()