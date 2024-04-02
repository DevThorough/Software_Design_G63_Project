import unittest, sys
from Software_Design_G63_Project.main import app #importing flask app object

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    def test_main_page(self):
        response = self.app.get('/', follow_redirect=True)
        self.assertEqual(response.status_code,200)  # add assertion here

    def test_register_page(self):
        response = self.app.get('/register', follow_redirect=True)
        self.assertEqual(response.status_code, 200)  # add assertion here

    def test_login_page(self):
        response = self.app.get('/login', follow_redirect=True)
        self.assertEqual(response.status_code, 200)  # add assertion here

    def test_fq_page(self):
        response = self.app.get('/fuel_quote', follow_redirect=True)
        self.assertEqual(response.status_code, 200)  # add assertion here
    def test_fqh_page(self):
        response = self.app.get('/fuel_quote_history', follow_redirect=True)
        self.assertEqual(response.status_code, 200)  # add assertion here
    def test_profile_page(self):
        response = self.app.get('/profile', follow_redirect=True)
        self.assertEqual(response.status_code, 200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
