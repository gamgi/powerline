from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    first_name = Column(String)
    username = Column(String, nullable=False)
    state = Column(String, default='unregistered', nullable=False)
    tos_accepted = Column(String)

    title = Column(String)
    age = Column(String)
    subscription = Column(String, default='normal')

    def __repr__(self):
        return 'user: {}'.format(id)
