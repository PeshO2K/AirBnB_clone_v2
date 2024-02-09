#!/usr/bin/python3
'''Module to run hello'''
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    '''hello message'''
    return("Hello HBNB!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
