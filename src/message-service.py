"""
messaging service.

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
    if 'message' and 'recipient-id' in request.POST:
        message = request.POST.get('message', None)
        recipient = request.POST.get('recipient-id', None)
        time_message_sent = datetime.datetime.now().time()
        fetched_messages[(message, recipient)] = time_message_sent
        return jsonify(
                        success=True,
                        recipient=recipient,
                        time_sent=time_message_sent)
    else:
        return jsonify(success=False, error_code=404), 404

@app.route('/fetch-messages/')
def fetch_messages():
    """
    Fetch messages not fetched previously

    Args:

    Return:

    """
    messages = []
    for message in messages:
        if message in fetch_messages.items():
            return jsonify(success=True, messages=messages)
    return jsonify(success=False, error=404), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
