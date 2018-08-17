from sqlalchemy import create_engine
from models import Base


def create_database(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(bind=engine)
