#!/usr/bin/python3
'''Module to run hello'''
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    '''hello message'''
    return("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    '''hello message'''
    return("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def ctext(text):
    '''hello message'''
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/<text>", strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def ptext(text='is cool'):
    '''hello message'''
    text = text.replace('_', ' ')
    return "Python {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
