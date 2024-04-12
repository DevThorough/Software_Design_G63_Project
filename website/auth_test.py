from main import app #importing flask app object
import unittest
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from unittest.mock import patch, MagicMock
from website.pricing import pricing, fuelPrice
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.profile import profileFunction
from .models import Profile
from website import db

class authTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
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
        #self.assertIn(b'Username must contain at least 2 characters', response.data)
        self.assertEqual(response.status_code, 500)
        invalid_resp = self.register('usernameistoolongforthisfield', 'user@gmail.com', 'pa')
        #self.assertIn(b'Password must contain at least 3 characters.', response.data)
        self.assertEqual(invalid_resp.status_code, 500)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code,200)  # add assertion here



if __name__ == '__main__':

    unittest.main()