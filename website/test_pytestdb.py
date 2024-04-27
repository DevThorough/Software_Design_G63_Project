from .models import Base, User, Profile, FuelQuote
from sqlalchemy import engine
from flask import Session

class TestDatabase:
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
        self.session.add(self.valid_user, self.valid_profile)
        self.session['userID'] = self.valid_user.id
        self.session['loggedIn'] = True
        self.session.commit()
        userProfile = Profile.query.filter_by(user_id=self.session['userID']).first()
        assert userProfile.id == 321
        assert userProfile.fullName == "Lebron James"