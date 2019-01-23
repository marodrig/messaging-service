"""
messaging service.
Submit message to a recipient by a given id.
Fetch messages not fetched previously
Fetch messages by time and return a slice between start and stop indeces.
Ordered by increasing or decreasing order.

"""
import datetime

from flask import Flask, abort, jsonify, request, url_for, make_response
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


@app.route('/messages/submit', methods=['POST'])
def submit_message():
    """
    Submits the given message to the intended recipient.
    add to database.

    Args:

    Return:

    """
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
        return jsonify(status_code=200, message=message.serialize)
    else:
        return jsonify(status_code=400, error="This service only accepts JSON data.")


@app.route('/messages/delete', methods=['DELETE'])
def delete_messages():
    """
    Delete messages.
    If given the message id, a single message is delete.
    If a recipient id is given, all messages sent to this recipient are deletes.

    Args:
        message-id(int): Message id of the message to be deleted
        recipient-id(String): Unique id of the recipient of all messages to be deleted.

    Returns:
        count_deleted(int): Number of messages deleted.

    """
    count_deleted = -100
    if 'message-id' in request.args:
        app.logger.debug("request arguments work.")
        message_id = request.args.get('message-id', None)
        count_deleted = session.query(Message).filter_by(id=message_id).delete()
        session.commit()
    elif 'recipient-id' in request.args:
        app.logger.debug("Deleting all messages to a specific recipient.")
        recipient_id = request.args.get('recipient-id', None)
        count_deleted = session.query(Message).filter(Message.recipient_id==recipient_id).delete()
        session.commit()

    if count_deleted >= 0:
        return jsonify(status_code=200, count=count_deleted)
    else:
        return jsonify(status_code=500, message="Error deleting messages.")



@app.route('/messages/fetch', methods=['GET'])
def fetch_messages():
    """
    Fetch messages not fetched previously
    Retrieve from datastore. use set to track previously fetched.

    Args:
        start-idx(int): starting index used to slice query result
        stop-idx(int): stop index used to slice query result

    Return:
        result(list): list of messages as specified in the query

    """
    messages = session.query(Message)
    result = []
    if 'start-idx' and 'stop-idx' in request.args:
        start_idx = int(request.args.get('start-idx', None))
        stop_idx = int(request.args.get('stop-idx', None))
        if stop_idx < start_idx:
            return jsonify(
                status_code=401,
                message='start-idx must be smaller than stop-idx.')
        try:
            result = messages.order_by('date_sent').slice(
                                                    start_idx,
                                                    stop_idx)
        except NoResultFound as nrfe:
            app.logger.error("No result found for query: {}".format(nrfe))
            abort(400)
    else:
        for message in messages.all():
            if message not in fetched_messages_set:
                fetched_messages_set.add(message)
                result.append(message)

    return jsonify(status_code=200, messages=[message.serialize for message in result])


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
