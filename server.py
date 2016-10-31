""" Rideshare App """

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

#**TD** Adjust once model.py is created
from model import *


app = Flask(__name__)

# Secret key - required for Flask Sessions and debug toolbar
app.secret_key = "thomothgromoth"

# Fail if Jinja uses undefined variable
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def indec():
    """Homepage"""

if __name__ == '__main__':
    # Debug for DebugToolbarExtension. Also so server restarts when changes made
    app.debug = True

    # Connection function from model.py
    connect_to_db(app)

    # Debug Toolbar
    DebugToolbarExtension(app)

    # Allows redirects
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True, host="0.0.0.0")