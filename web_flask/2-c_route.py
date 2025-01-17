#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when the root URL is accessed.

    Returns:
        str: A greeting message.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB" when the /hbnb URL is accessed.

    Returns:
        str: A message containing "HBNB".
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Displays "C " followed by the value of the text variable.

    Args:
        text (str): The value to be displayed.

    Returns:
        str: The formatted message.
    """
    return "C {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    """
    Runs the Flask application on 0.0.0.0:5000.

    Debug mode is disabled.
    """
    app.run(host="0.0.0.0", port=5000, debug=None)
