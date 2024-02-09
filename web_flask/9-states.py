#!/usr/bin/python3
"""
Flask web application with storage engine integration.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """
    Close the storage session after each request.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """
    Route handler for /states and /states/<id>.
    """
    states = storage.all(State).values()
    filtered = False

    if id:
        # filter state matching id
        states = next((state for state in states if state.id == id), None)
        filtered = True
        # return render_template('9-states.html', states=state, filtered=True)

    return render_template('9-states.html', states=states, filtered=filtered)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
