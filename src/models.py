"""
ORM model for a message.

"""
import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import (NoResultFound, ObjectDeletedError,
                                StaleDataError)


engine = create_engine('sqlite:///datastore.db')
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()


class InternalServerError(Exception):
    """
    """
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.__class__.__name__
        rv['message'] = self.message
        return rv


class NotAcceptable(Exception):
    """
    """
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.__class__.__name__
        rv['message'] = self.message
        return rv


class NotFound(Exception):
    """
    """
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.__class__.__name__
        rv['message'] = self.message
        return rv


class InvalidUsage(Exception):
    """
    Exception class for invalid usage of the API

    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """
        """
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.__class__.__name__
        rv['message'] = self.message
        return rv

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
    Message from user

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
            'messageText': self.message_text,
            'recipientId': self.recipient_id,
            'dateSent': self.date_sent}

    @classmethod
    def get(cls, request):
        """
        HTTP GET request

        """

        messages_qs = session.query(cls)
        result = []
        if 'Accept' in request.headers and 'application/json' not in request.headers.get('Accept', '').split(';'):
            raise NotAcceptable('This API only supports application/json media type.', 406)
        if 'startIdx' and 'stopIdx' in request.args:
            start_idx = int(request.args.get('startIdx'))
            stop_idx = int(request.args.get('stopIdx'))
            if stop_idx < start_idx:
                raise InvalidUsage('stopIdx must be greater than startIdx',
                                   400)
            try:
                result = messages_qs.order_by('date_sent').slice(
                                                    start_idx,
                                                    stop_idx)
            except NoResultFound:
                raise NotFound('Query returned no messages.', 404)
        else:
            try:
                result = messages_qs.all()
            except NoResultFound:
                raise NotFound('Query returned no messages', 404)
        if result:
            return [message.serialize for message in result]
        else:
            raise NotFound('Query return no messages.', 404)

    @classmethod
    def post(cls, request):
        """
        HTTP POST request

        """
        if request.is_json:
            data = request.get_json()
            message = cls(
                message_text=data.get('message', None),
                recipient_id=data.get('recipientId', None)
            )
            return message
        else:
            raise InvalidUsage('This service only accepts JSON data.', 400)

    @classmethod
    def delete(cls, request):
        """
        """
        count_deleted = None
        if 'messagesId' in request.args:
            messages_ids = map(int, request.args.get('messagesId').split(','))
            for message_id in messages_ids:
                try:
                    count_deleted = session.query(cls).filter_by(id=message_id).delete()
                    session.commit()
                except ObjectDeletedError:
                    raise NotFound(
                        'No message exists for messageId: {}'.format(message_id),
                        404)
                except StaleDataError as sde:
                    raise InternalServerError(
                        sde,
                        500
                    )
        return {'deletedCount': count_deleted}


engine = create_engine('sqlite:///datastore.db')
Base.metadata.create_all(engine)
