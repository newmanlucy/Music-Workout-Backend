import unittest
from util import client_log
from datetime import datetime

from client import post_user, get_user, delete_user

class TestUser(unittest.TestCase):

    
    # Test adding users
    birthday = "11/20/1996"

    def test_add_user_no_username(self):
        r = post_user(None, self.birthday)
        self.assertEqual(r.status_code, 400)

    def test_add_user_no_bday(self):
        r = post_user("lindsey", None)
        self.assertEqual(r.status_code, 400)

    def test_add_user_not_unique(self):
        post_user("rachel", self.birthday)
        r = post_user("rachel", datetime.now())
        self.assertEqual(r.status_code, 400)

    def test_add_user_success(self):
        delete_user("emily")
        r = post_user("emily", self.birthday)
        client_log(r.json())
        self.assertEqual(r.status_code, 200)


    # # Test getting users
    
    def test_get_user_not_there(self):
        delete_user("harrypotter")
        r = get_user("harrypotter")
        self.assertEqual(r.status_code, 404)

    def test_get_user_success(self):
        post_user("francis", self.birthday)
        r = get_user("francis")
        self.assertEqual(r.status_code, 200)


    # # Test deleting users
    
    def test_delete_user_not_there(self):
        r = delete_user("lauren")
        self.assertEqual(r.status_code, 404)

    def test_delete_user_success(self):
        post_user("megan", self.birthday)
        r = delete_user("megan")
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
