import testing.postgresql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import create_database
import models

# Postgresql = testing.postgresql.PostgresqlFactory(
#    cache_initialized_db=True)


class fake_database(object):
    def __init__(self):
        # Postgresql class which shares the generated test database
        self.db = testing.postgresql.Postgresql()
        self.db_engine = create_engine(self.db.url())

    @property
    def engine(self):
        return self.db_engine

    def __del__(self):
        self.stop()

    def stop(self):
        self.db.stop()
        # Postgresql.clear_cache()


def create_database_fixture(db_engine, setup='simple_one_user'):
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
