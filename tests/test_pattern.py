import unittest
from util import client_log
from datetime import datetime

from client import post_user, delete_user, post_pattern, get_patterns, delete_pattern

class TestPattern(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r1 = delete_user("lucy")
        r2 = post_user("lucy", datetime.now())
        print(r1)
        print(r2.json())
        cls.user_id = r2.json()["user_id"]
        cls.very_high_number = 10000000

    @classmethod
    def tearDownClass(cls):
        delete_user("lucy")

    # Test posting patterns
    def test_post_pattern_no_user_id(self):
        r = post_pattern(None, [1,2,3], True)
        self.assertEqual(r.status_code, 400)

    def test_post_pattern_no_pattern(self):
        r = post_pattern(55, None, True)
        self.assertEqual(r.status_code, 400)

    def test_post_pattern_no_default(self):
        r = post_pattern(55, [1,2,3], None)
        self.assertEqual(r.status_code, 400)

    @unittest.skip("TODO")
    def test_post_pattern_key_constraint_fails(self):
        r = post_pattern(self.very_high_number, [1,2,3], True)
        self.assertEqual(r.status_code, 400)

    def test_post_pattern_success(self):
        r = post_pattern(self.user_id, [1,2,3], False)
        self.assertEqual(r.status_code, 200)


    # Test getting patterns

    def test_get_patterns_succes(self):
        r = get_patterns(self.user_id)
        self.assertEqual(r.status_code, 200) 

    
    # Test deleting patterns

    def test_delete_pattern_not_in_database(self):
        r = delete_pattern(self.very_high_number)
        self.assertEqual(r.status_code, 404)

    def test_delete_pattern_success(self):
        r1 = post_pattern(self.user_id, [1,2,3], True)
        print("r1")
        print(r1.json())
        pattern_id = r1.json()["pattern_id"]
        r2 = delete_pattern(pattern_id)
        self.assertEqual(r2.status_code, 200)


if __name__ == '__main__':
    unittest.main()