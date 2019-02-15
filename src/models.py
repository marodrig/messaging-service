"""
ORM model for a message.

"""
import datetime
# import os
# import sys

from sqlalchemy import (Column, DateTime, Integer, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Link(Base):
#     """
#     """
#     __tablename__ = 'link'
#     rel = Column(String(64), nullable=False)
#     href = Column(String(64), nullable=False)
#     action = Column(String(64), nullable=False)
#     _types = Column(String(128))

#     @property
#     def types(self):
#         return [type for type in self._types.split(';') if type]

#     @types.setter
#     def types(self, value):
#         self._types += "{};".format(value)


# class Operation(Base):
#     """
#     """
#     __tablename__ = 'operation'


class Message(Base):
    """
    """
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    message_text = Column(String(140), nullable=False)
    recipient_id = Column(String(256), nullable=False)
    date_sent = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """
        """
        return {
            'id': self.id,
            'message_text': self.message_text,
            'recipiend_id': self.recipient_id,
            'date_sent': self.date_sent}


engine = create_engine('sqlite:///datastore.db')
Base.metadata.create_all(engine)
