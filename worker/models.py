from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    first_name = Column(String)
    username = Column(String, nullable=False)
    #registered = Column(DateTime, default=func.now(), nullable=False)
    state = Column(String, default='unregistered', nullable=False)
    title = Column(String)
    age = Column(String)
    subscription = Column(String, default='normal')
    #chat_id = Column(String, nullable=False)

    """
    @validates('id')
    def validate_id(self, key, id):
        assert id != None
        return id

    @validates('state')
    def validate_id(self, key, state):
        assert state != None
        return state
    """

    def __repr__(self):
        return 'user: {}'.format(id)
