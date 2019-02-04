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
from models import Message
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

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
                return jsonify(message='Resource not created.', error=ie), 204
            return jsonify(message=message.serialize), 201
        else:
            return jsonify(error="This service only accepts JSON data."), 400
    elif request.method == 'GET':
        messages_qs = session.query(Message)
        result = []
        if 'start-idx' and 'stop-idx' in request.args:
            start_idx = int(request.args.get('start-idx'))
            stop_idx = int(request.args.get('stop-idx'))
            if stop_idx < start_idx:
                return jsonify(
                    message='start-idx must be smaller than stop-idx.'), 401
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
            return jsonify(messages=[message.serialize for message in result]), 200
        else:
            return jsonify(error="No new messages to fetch."), 404
    elif request.method == 'DELETE':
        count_deleted = None
        if 'message-id' in request.args:
            app.logger.debug("request arguments work.")
            message_id = request.args.get('message-id')
            count_deleted = session.query(Message).filter_by(id=message_id).delete()
            session.commit()
        elif 'recipient-id' in request.args:
            app.logger.debug("Deleting all messages to a specific recipient.")
            recipient_id = request.args.get('recipient-id')
            count_deleted = session.query(Message).filter(Message.recipient_id == recipient_id).delete()
            session.commit()

        if count_deleted:
            return jsonify(count=count_deleted), 204
        else:
            return jsonify(message="Error deleting messages."), 500
    return jsonify(message='Not a supported action.'), 400


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
