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


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Function Documentation: Route handler for /states_list.
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
