#!/usr/bin/python3
"""
Module Documentation: Flask web application with storage engine integration.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """
    Function Documentation: Close the storage session after each request.
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Function Documentation: Route handler for /cities_by_states.
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
