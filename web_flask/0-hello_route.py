#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when the root URL is accessed.

    Returns:
           A given string
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    """
    Runs the Flask application on 0.0.0.0:5000.

    Debug mode is disabled.

    To test the application, open a web browser and go to http://0.0.0.0:5000/
    """
    app.run(host="0.0.0.0", port=5000, debug=None)
