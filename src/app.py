"""
messaging service.
Submit message to a recipient by a given id.
Fetch messages not fetched previously
Fetch messages by time and return a slice between start and stop indeces.
Ordered by increasing or decreasing order.

"""
import datetime

from flask import (Flask, Response, abort, jsonify, make_response, request,
                   url_for)
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models import InvalidUsage, Message, NotAcceptable, NotFound, InternalServerError

app = Flask(__name__)

engine = create_engine('sqlite:///datastore.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()
fetched_messages_set = set()


@app.route('/v1/messages', methods=['POST', 'GET', 'DELETE'])
def message_endpoint():
    """
    Submits the given message to the intended recipient.
    add to database.

    Args:

    Return:

    """
    resp = None
    if request.method == 'POST':
        try:
            message = Message.post(request)
            session.add(message)
            session.commit()
        except IntegrityError as ie:
            app.logger.error("Data integrity error: {}".format(ie))
            return make_response(
                    jsonify(message='Resource not created.', error=ie),
                    500)
        except InvalidUsage:
            raise
        resp = make_response(
            jsonify(message=message.serialize),
            201)
        resp.headers['Content-Type'] += '; charset=utf-8'
        resp.headers['Location'] = '/v1/messages/{}'.format(message.id)
        return resp
    elif request.method == 'GET':
        try:
            messages = Message.get(request)
        except (NotFound, InvalidUsage, NotAcceptable):
            raise
        resp = make_response(
            jsonify(messages),
            200)
        resp.headers['Content-Type'] += '; charset=utf-8'
        return resp
    elif request.method == 'DELETE':
        try:
            delete_count = Message.delete(request)
        except (NotFound, InternalServerError):
            raise
        resp = make_response(
            jsonify(delete_count),
            204)
        resp.headers['Content-Type'] += '; charset=utf-8'
        return resp

@app.errorhandler(InternalServerError)
def handle_internal_server_error(error):
    """
    """
    return make_response(
        jsonify(error=error.to_dict()),
        error.status_code
    )

@app.errorhandler(NotAcceptable)
def handle_not_acceptable(error):
    """
    """
    response = make_response(
        jsonify(error=error.to_dict()),
        error.status_code
    )
    return response

@app.errorhandler(NotFound)
def handle_not_found(error):
    """
    """
    response = make_response(
        jsonify(error=error.to_dict()),
        error.status_code
    )
    return response

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    Correct handling of the InvalidUsage exception

    """
    response = make_response(
        jsonify(error=error.to_dict()),
        error.status_code)
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
