from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_filter_users(): # Create a mock session object
session = MagicMock()

    # Create a mock query object and configure it to return a list of users
    query = MagicMock()
    query.filter.return_value = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    session.query.return_value = query

    # Call the function being tested
    result = filter_users(session, name='John')

    # Assert that the function returned the expected result
    assert result == [{'id': 1, 'name': 'John'}]
    # Assert that the filter method was called with the correct arguments
    query.filter.assert_called_with(User.name == 'John')