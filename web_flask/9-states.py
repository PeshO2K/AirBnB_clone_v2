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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """
    Function Documentation: Route handler for /states and /states/<id>.
    """
    states = storage.all(State).values()

    if id:
        # filter state matching id
        state = next((state for state in states if state.id == id), None)
        return render_template('9-states.html', states=state, filtered=True)

    return render_template('9-states.html', states=states, filtered=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
