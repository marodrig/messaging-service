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

You need to start the Flask app using the following command:

> pipenv

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
| /submit-message/ | POST | submit given message to recipient with given id. | message-txt, recipient-id | {status=200, time-submitted=, message=, recipient=}|
| /fetch-messages/ | GET | Fetch messages not yet fetched. | time-ordered, start-idx, stop-idx | {status=200, messages=[{time-submitted=, message=, recipient=}, {time-submitted=, message=, recipient=}]} |
| /delete-message/ | DELETE | Delete one or more messages. | messages | {status=200, deleted-messages-count=10}|

## Running tests

## FAQ

## Contributing

## Credits or References

## License
