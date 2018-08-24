from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    username = Column(String, nullable=False)
    registered = Column(DateTime, default=func.now(), nullable=False)
    state = Column(String, default='unregistered', nullable=False)
    title = Column(String)
    #chat_id = Column(String, nullable=False)

    def __repr__(self):
        return 'user: {}'.format(self.id, self.username)
