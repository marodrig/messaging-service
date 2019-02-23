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
from src.models import Message
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import (NoResultFound, ObjectDeletedError,
                                StaleDataError)

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
        if request.is_json:
            data = request.get_json()
            message = Message(
                message_text=data.get('message', None),
                recipient_id=data.get('recipient-id', None)
            )
            session.add(message)
            try:
                session.commit()
            except IntegrityError as ie:
                app.logger.error("Data integrity error: {}".format(ie))
                return make_response(
                        jsonify(message='Resource not created.', error=ie),
                        204)
            resp = make_response(
                        jsonify(message=message.serialize),
                        201)
            resp.headers['Content-Type'] += '; charset=utf-8'
            resp.headers['Location'] = '/v1/messages/{}'.format(message.id)
            return resp
        else:
            resp = make_response(
                    jsonify(error={'message': 'This service only accepts JSON data.'}),
                    400)
            return resp
    elif request.method == 'GET':
        messages_qs = session.query(Message)
        result = []
        if 'Accept' in request.headers and 'application/json' not in request.headers.get('Accept', '').split(';'):
            resp = make_response(
                    jsonify(error={'message': 'This API support application/json media type.'}),
                    406)
            return resp
        if 'start-idx' and 'stop-idx' in request.args:
            start_idx = int(request.args.get('start-idx'))
            stop_idx = int(request.args.get('stop-idx'))
            if stop_idx < start_idx:
                return make_response(
                        jsonify(message='start-idx must be smaller than stop-idx.'),
                        400)
            try:
                result = messages_qs.order_by('date_sent').slice(
                                                    start_idx,
                                                    stop_idx)
            except NoResultFound as nrfe:
                app.logger.error("No result found for query: {}".format(nrfe))
                abort(404)
        else:
            try:
                message_lst = messages_qs.all()
            except NoResultFound as nrfe:
                app.logger.error("No result found for query: {}".format(nrfe))
                abort(404)
            for message in message_lst:
                if message not in fetched_messages_set:
                    fetched_messages_set.add(message)
                    result.append(message)
        if result:
            return make_response(
                    jsonify(messages=[message.serialize for message in result]),
                    200)
        else:
            return jsonify(error="No new messages to fetch."), 404
    elif request.method == 'DELETE':
        count_deleted = None
        if 'messages-id' in request.args:
            messages_ids = map(int, request.args.get('messages-id').split(','))
            app.logger.debug("ids passed to delete: {}".format(messages_ids))
            for message_id in messages_ids:
                try:
                    count_deleted = session.query(Message).filter_by(id=message_id).delete()
                    session.commit()
                except ObjectDeletedError as ode:
                    app.logger.error(ode)
                    abort(404)
                except StaleDataError as sde:
                    app.logger.error(sde)
                    abort(500)
        if count_deleted:
            return make_response(
                    jsonify(count=count_deleted),
                    204)
        else:
            return make_response(
                    jsonify(message="Error deleting messages."),
                    500)
    return make_response(
                jsonify(message='Not a supported action.'),
                400)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
