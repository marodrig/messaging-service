# Messaging Service

Messaging service for sending and retrieving text messages implemented using a REST-API.

## Table of contents

## What is the reason for this project?

Create a messaging service using Flask that sends and retrieve text messages.

## Why should you care about this project?

You are looking for a messaging service written in Python.

## Features

This service has four main functions:

- Submits a text message  to a recipient, where the recipient is identified using email, phone number or other id.
- Fetches not previously fetched messages.
- Delete on or more messages.
- Fetches a slice (between start index and stop index) of all messages (including previously fetched ones) ordered by time.

This service does not handle authorization or authentication.

Package management for this project is done using pipenv.

## Installation & Quick start

This service was developed and tested in a Linux/OSX environment and the installation and quick start guide assumes you are working in a Linux/OSX environment.

### Cloning the project from github

You will need to clone the project source code to your machine

> git clone https://github.com/marodrig/messaging_service_app

### Built with & Requirements

- Python
- Homebrew
- pyenv
- pipenv
- Flask

#### Installing Homebrew on OSX

In order to install Homebrew on OSX you can simply copy the following command on the terminal

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

More info on Homebrew:

[https://brew.sh/](https://brew.sh/)

#### Installing pyenv

You can use homebrew to install pyenv on OSX:

> $ brew install pyenv

More info on pyenv:

[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

#### Installing pipenv

You know how pip and virtualenv are basic tools for Python development? Wouldn't it be nice if we had something that merged both? pipenv is the answer.

The best way to install pipenv on OSX is to use homebrew:

> $ brew install pipenv

More info about pipenv:

[https://pipenv.readthedocs.io/en/latest/](https://pipenv.readthedocs.io/en/latest/)

#### Using pipenv to install Flask and other dependencies

This repository includes a pipfile, we can use the pipfile similarly to a requirements.txt file in pip.  We can simply type the following command in the command line to install our dependencies.

> $ pipenv install

#### Security check with pipenv

> pipenv check

## Usage

First start your sqlite3 database by typing:

> pipenv run python src/database.py

You need to start the Flask app using the following command:

> pipenv run python src/message-service.py

The messaging service will be running in localhost at port 8080, and can be tested using curl from the command line on OSX:

Submit a message to a recipient:

> curl 'localhost:8080/messages/submit' -d '{"message": "bar", "recipient-id":123}' -H 'Content-Type: application/json'

Fetch a slice of all messages ordered by time between start-idx and stop-idx(non-inclusive)

> curl 'localhost:8080/messages/fetch?start-idx=1&stop-idx=4'

Fetch all non-yet-fetch messages:

>curl 'localhost:8080/messages/fetch'

Delete a message with message-id:

> curl 'localhost:8080/messages/delete?message-id=100' -i -X DELETE

Delete a message with recipient-id:

> curl 'localhost:8080/messages/delete?recipient-id=100' -i -X DELETE

## REST-API reference

### Status codes

| Status code | Meaning  |
|:---:|:---|
|  200 | OK  |
| 400 | Client side error. |
|  403 | Forbidden, this service is HTTP only.    |
|  500 | Server side error. |

### End-point reference

| URL | HTTP Method | action | arguments | response example |
| :--- | :---: | :---: | :--- | :---: |
| /messages/submit?message="bar"&recipient-id=123 | POST | submit given message to recipient with given id. | message, recipient-id | {"message": {"date_sent": "Wed, 23 Jan 2019 18:09:52 GMT", "id": 5,"message_text": "bar", "recipiend_id": "123"},"status": 200}|
| /messages/fetch | GET | Fetch messages not yet fetched. | None| {"messages": [{"date_sent": "Wed, 23 Jan 2019 17:15:03 GMT", "id": 1, "message_text": "bar", "recipiend_id": "123"}], "status_code":200} |
| /messages/delete?message-id=1 | DELETE | Delete one one message with id equal to message_id | message_id | {"message": 1, "status_code": 200}|
| /messages/delete?recipient-id=123> | DELETE | Delete one one message with id equal to message_id | message_id | {"message": 1, "status_code": 200}|
| /messages/fetch?start-idx=1&stop_idx=5 | GET | Fetch a slice of messages  between start-idx and stop-idx ordered by time from oldest to newest. | start-idx, stop-idx | {"messages": [{"date_sent": "Wed, 23 Jan 2019 17:15:03 GMT", "id": 1, "message_text": "bar", "recipiend_id": "123"}, {"date_sent": "Wed, 23 Jan 2019 17:27:05 GMT", "id": 2, "message_text": "bar", "recipiend_id": "123"} ],"status_code": 200}|

## Running tests

## FAQ

## Contributing

## Credits or References

## License
