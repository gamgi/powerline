from sqlalchemy.orm import sessionmaker
from create_database import create_database
import models


def create_mock_database(db_engine, setup='simple_one_user'):
    assert db_engine is not None
    create_database(db_engine=db_engine)

    # Insert mock data
    if setup == 'simple_one_user':
        user = models.User(
            id='123',
            username='gary56',
            first_name='Gary')
        session = sessionmaker(bind=db_engine)()
        session.add(user)
        session.commit()
        session.close()
