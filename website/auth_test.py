from website.__init__ import create_app, db
import unittest
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from unittest.mock import patch, MagicMock
from website.pricing import fuelPrice
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.profile import profileFunction
from website.models import Profile


app = create_app()


class authTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register(self, username, password):
        return self.app.post('/register',
                             data=dict(username=username,
                                       password=password),
                             follow_redirects=True)
    def test_valid_user_registration(self):
        response=self.register('test','FlaskIsAwesome')
        self.assertEqual(response.status_code,200)

    def test_invalid_registration(self):
        response = self.register('t','FlaskIsAwesome')
        #self.assertIn(b'Username must contain at least 2 characters', response.data)
        self.assertEqual(response.status_code, 500)
        invalid_resp = self.register('usernameistoolongforthisfield','pa')
        #self.assertIn(b'Password must contain at least 3 characters.', response.data)
        self.assertEqual(invalid_resp.status_code, 500)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code,200)  # add assertion here


class ProfileFunctionTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()  # Push application context

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Register a user for testing
            new_user = User(username='test_user',
                            password=generate_password_hash('test_password', method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            # Log in the user
            response = self.app.post('/login', data=dict(username='test_user', password='test_password'),
                                     follow_redirects=True)
            self.assertIn(b'Logged in successfully!', response.data)  # Verify successful login

    def tearDown(self):
        self.app_context.pop()  # Pop application context
        #with self.app as client:
            #with client.session_transaction() as sess:
                #sess['loggedIn'] = False
                #sess['userID'] = 123  # Set userID in session

    def test_get_profile_when_authenticated(self):
        # Simulate an authenticated session
        with self.app as client:
            with client.session_transaction() as sess:
                #sess['loggedIn'] = True
                sess['userID'] = 123  # Set userID in session

            # Mock the profile query
            with patch('website.profile.Profile.query.filter_by') as mock_filter_by:
                # Mock the profile
                mock_profile = MagicMock()
                mock_profile.fullName = 'John Doe'
                mock_profile.address1 = '123 Main St'
                mock_profile.address2 = ''
                mock_profile.city = 'Anytown'
                mock_profile.state = 'CA'
                mock_profile.zipCode = '12345'
                mock_filter_by.return_value.first.return_value = mock_profile

                # Make a request to the profile endpoint
                response = client.get('/profile', follow_redirects=True)
                self.assertIn(b'John Doe', response.data)


class TestFuelPrice(unittest.TestCase):

    def setUp(self):
        self.userID = 1234
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()  # Push application context

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Register a user for testing
            new_user = User(username='test_user',
                            password=generate_password_hash('test_password', method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            new_profile = Profile(id=1,fullName="John Doe",address1="123 Main St",address2="Apt 101",
                                  city="Anytown",state="NY",zipCode="12345",
                                  user_id=123)

            db.session.add(new_profile)
            db.session.commit()

            # Log in the user
            response = self.app.post('/login', data=dict(username='test_user', password='test_password'),
                                     follow_redirects=True)
            self.assertIn(b'Logged in successfully!', response.data)  # Verify successful login

    def test_fuel_price(self):
        # Test with gallons less than 100 and no delivery date
        price = fuelPrice(50, False, 123)
        self.assertAlmostEqual(price, round(1.755,2))  # Expected price without discount


    def test_negative_gallons(self):
        # Test with negative gallons (should raise ValueError)
        with self.assertRaises(ValueError):
            fuelPrice(-50, False, self.userID)

if __name__ == '__main__':

    unittest.main()