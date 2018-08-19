from sqlalchemy import create_engine
from models import Base


def create_database(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(bind=engine)


# When starting the docker container, this file is executed
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
