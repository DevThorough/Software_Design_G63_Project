from models import Base, User, Profile, FuelQuote
from sqlalchemy import engine
from flask import Session

class TestBlog:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_user = User(
            id=1234,
            username="abc",
            password="123"
        )
        self.valid_profile = Profile(
            id=321,
            fullName="Lebron James",
            address1="123 main st",
            address2="Unit #100",
            city="Houston",
            state="TX",
            zipCode="77000",
            user_id=1234
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_author_valid(self):   
        self.session.add(self.valid_author)
        self.session.commit()
        aybak = self.session.query(Author).filter_by(lastname="Aybak").first()
        assert aybak.firstname == "Ezzeddin"
        assert aybak.lastname != "Abdullah"
        assert aybak.email == "aybak_email@gmail.com"