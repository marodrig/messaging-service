"""
messaging service.
Submit message to a recipient by a given id.
Fetch messages not fetched previously
Fetch messages by time and return a slice between start and stop indeces.
Ordered by increasing or decreasing order.

"""
import datetime
from flask import Flask, abort, jsonify, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Message


app = Flask(__name__)

engine = create_engine('sqlite:///datastore.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()
fetched_messages_set = set()


@app.route('/submit/', methods=['POST'])
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
        return jsonify(status=200, message=message.serialize)
    else:
        return jsonify(status=400, error="This service only accepts JSON data.")


@app.route('/messages/', methods=['GET'])
def fetch_messages():
    """
    Fetch messages not fetched previously
    Retrieve from datastore. use set to track previously fetched.

    Args:

    Return:

    """
    messages = session.query(Message).all()
    result = []
    for message in messages:
        if message not in fetched_messages_set:
            fetched_messages_set.add(message)
            result.append(message)
    if 'ordered-by-time' in request.args:
        result = session.query(Message).order_by('date_sent').all()
        if 'start-idx' and 'stop-idx' in request.args:
            start_idx = request.args.get('start-idx', None)
            stop_idx = request.args.get('stop-idx', None)
            result = session.query(Message).order_by('date_sent').slice(start_idx, stop_idx)

    return jsonify(status=200, messages=[message.serialize for message in result])
    # if 'start-idx' and 'stop-idx' in request.args:
    #     start_idx = request.args.get('start-idx', None)
    #     stop_idx = request.args.get('stop-idx', None)
    #     app.logger.debug('start-idx in HTTP request.')
    #     app.logger.debug('start-idx: {0}'.format(start_idx))
    #     app.logger.debug('start-idx: {0}'.format(stop_idx))
        #TODO query all messages, order by time return splice[start_idx:stop_idx]
    # return jsonify(status=200, messages=['Great!', 'Awesome'])
    # messages = []
    # for message in messages:
    #     if message in fetch_messages.items():
    #         return jsonify(success=True, messages=messages)
    # return jsonify(success=False, error=404), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
