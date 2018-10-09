""" PTSD Project """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db

app = Flask(__name__)

# app.secret_key is required to use Flask sessions and the debug toolbar
app.secret_key = 'temporary_secret_key'

# set the following so that if an undefined variable is used in Jinja2,
# it doesn't fail silently
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """ Homepage. """

    return render_template('homepage.html')

if __name__ == '__main__':
    # debug must be set to True at the point that DebugToolbarExtension is invoked
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')