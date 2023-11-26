#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template

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


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False, defaults={'text': 'is cool'})
def python_text(text):
    """
    Displays "Python " followed by the value of the text variable.

    Args:
        text (str): The value to be displayed.

    Returns:
        str: The formatted message.
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Displays "n is a number" only if n is an integer.

    Args:
        n (int): The number to be checked.

    Returns:
        str: A message indicating whether n is a number.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Displays an HTML page with a header tag
    containing "Number: n" if n is an integer.

    Args:
        n (int): The number to be displayed.

    Returns:
        str: HTML page.
    """
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    """
    Runs the Flask application on 0.0.0.0:5000.

    Debug mode is disabled.
    """
    app.run(host="0.0.0.0", port=5000, debug=None)
