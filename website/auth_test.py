import unittest
from Software_Design_G63_Project.main import app #importing flask app object
from Software_Design_G63_Project.website.__init__ import db

class authTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client_class()
        db.drop_all()
        db.create_all()
    def register(self, username, email, password):
        return self.app.post('/register',
                             data=dict(username=username,
                                       email=email,
                                       password=password,
                                       confirm_password=password),
                             follow_redirects=True)
    def test_valid_user_registration(self):
        response=self.register('test','test@example','FlaskIsAwesome')
        self.assertEqual(response.status_code,200)

    def test_invalid_registration(self):
        response = self.register('t', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Username must contain at least 2 characters', response.data)
        invalid_resp = self.register('usernameistoolongforthisfield', 'user@gmail.com', 'pa')
        self.assertIn(b'Password must contain at least 3 characters.', response.data)




if __name__ == '__main__':
    unittest.main()
