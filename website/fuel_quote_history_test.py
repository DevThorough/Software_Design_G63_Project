import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models import Base

class Panel(Base):
    # ...

    def __eq__(self, other):
        return isinstance(other, Panel) and other.id == self.id
    class TestQuery(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.panel = Panel(1, 'ion torrent', 'start')
        self.session.add(self.panel)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_panel(self):
        expected = [self.panel]
        result = self.session.query(Panel).all()
        self.assertEqual(result, expected)