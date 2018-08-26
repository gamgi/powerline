from sqlalchemy import create_engine
from models import Base
import config


def create_database(uri='postgres://postgres', db_engine=None):
    """Creates database schema.

    Accepts db URI or engine as parameter.
    """
    if db_engine is None:
        db_engine = create_engine(uri)
    if config.DEVELOPMENT:
        print('...deleteing old database because DEVELOPMENT=1')
        # Delete schem
        Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(bind=db_engine)


# When starting the docker container (for development)
# this file is executed to ensure the db has a schema
if __name__ == "__main__":
    from config import SQLALCHEMY_DATABASE_URI
    from sys import exit
    from time import sleep
    from sqlalchemy.exc import OperationalError
    attempts = 3
    print('attempting to create database at {}'.format(SQLALCHEMY_DATABASE_URI))
    for attempt in range(attempts):
        try:
            create_database(SQLALCHEMY_DATABASE_URI)
            print('...success')
            break
        except OperationalError:
            if (attempt == attempts - 1):
                print('...unable to connect')
                exit(1)
            print('...db not ready yet')
            sleep(4)
            continue
