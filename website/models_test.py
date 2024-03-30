## example sqlalchemy tests
import unittest
from myapp import db, User

class TestDb(unittest.TestCase):
    def setUp(self):
        db.init_app('sqlite://')
        db.create_all()
        db.session.add(User(name='Cristian'))
        db.commit()

    def test_it(self):
        user = User.query.filter_by(name='Cristian')
        assert user is not None

    def tearDown(self):
        # TODO: clean up your test