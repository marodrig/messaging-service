"""
messaging service.
Submit message to a recipient by a given id.
Fetch messages not fetched previously
Fetch messages by time and return a slice between start and stop indeces.
Ordered by increasing or decreasing order.

"""
import datetime
from flask import Flask, abort, jsonify, request, url_for


app = Flask(__name__)
fetched_messages = {}


@app.route('/submit/', methods=['POST'])
def submit_message(message):
    """
    Submits the given message to the intended recipient.

    Args:

    Return:

    """
    if 'message' and 'recipient-id' in request.args:
        request_json = request.get_json()
        message = request_json.get('message', None)
        recipient = request_json.get('recipient-id', None)
        time_message_sent = datetime.datetime.now().time()
        fetched_messages[(message, recipient)] = time_message_sent
        return jsonify(
                        status=200,
                        recipient=recipient,
                        time_sent=time_message_sent)
    else:
        return jsonify(status=404, error='Error')


@app.route('/fetch-messages/', methods=['GET'])
def fetch_messages():
    """
    Fetch messages not fetched previously

    Args:

    Return:

    """
    if 'start-idx' and 'stop-idx' in request.args:
        start_idx = request.args.get('start-idx', None)
        stop_idx = request.args.get('stop-idx', None)
        app.logger.debug('start-idx in HTTP request.')
        app.logger.debug('start-idx: {0}'.format(start_idx))
        app.logger.debug('start-idx: {0}'.format(stop_idx))
    return jsonify(status=200, messages=['Great!', 'Awesome'])
    # messages = []
    # for message in messages:
    #     if message in fetch_messages.items():
    #         return jsonify(success=True, messages=messages)
    # return jsonify(success=False, error=404), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
