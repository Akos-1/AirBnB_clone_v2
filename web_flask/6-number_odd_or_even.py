#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays "Hello HBNB!" when the root URL is accessed."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays "HBNB" when the /hbnb URL is accessed."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Displays "C " followed by the value of the text variable."""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False, defaults={'text': 'is cool'})
def python_text(text):
    """Displays "Python " followed by the value of the text variable."""
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Displays "n is a number" only if n is an integer."""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays an HTML page with a header tag
    containing 'Number: n' if n is an integer."""
    return render_template('number_template.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Displays an HTML page with a header tag
    indicating if n is even or odd."""
    return render_template(
        'number_odd_or_even.html',
        number=n,
        result='even' if n % 2 == 0 else 'odd')


if __name__ == "__main__":
    """Runs the Flask application on 0.0.0.0:5000. Debug mode is disabled."""
    app.run(host="0.0.0.0", port=5000, debug=None)
