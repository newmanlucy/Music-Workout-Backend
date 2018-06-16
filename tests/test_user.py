import unittest
from util import client_log

from client import post_user, get_user, delete_user

class TestUser(unittest.TestCase):

    
    # Test adding users

    def test_add_user_no_username(self):
        r = post_user(None, 21)
        self.assertEqual(r.status_code, 400)

    def test_add_user_no_age(self):
        r = post_user("lindsey", None)
        client_log(r.json())
        self.assertEqual(r.status_code, 400)

    def test_add_user_not_unique(self):
        post_user("rachel", 12)
        r = post_user("rachel", 15)
        self.assertEqual(r.status_code, 400)

    def test_add_user_success(self):
        r = post_user("emily", 17)
        self.assertEqual(r.status_code, 200)


    # Test getting users
    
    def test_get_user_not_there(self):
        delete_user("harrypotter")
        r = get_user("harrypotter")
        self.assertEqual(r.status_code, 404)

    def test_get_user_success(self):
        post_user("harrypotter")
        r = get_user("harrypotter")
        self.assertEqual(r.status_code, 200)


    # Test deleting users
    
    def test_delete_user_not_there(self):
        delete_user("rachel")
        delete_user("emily")
        r = delete_user("emily")
        self.assertEqual("r.status_code", 404)

    def test_delete_user_success(self):
        add_user("lindsey")
        r = delete_user("lindsey")
        self.assertEqual(r.status_code, 404)


if __name__ == '__main__':
    unittest.main()