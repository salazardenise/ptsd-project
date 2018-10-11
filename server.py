""" PTSD Project """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
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
    """ Display omepage. """

    return render_template('homepage.html')

@app.route('/signup', methods=['GET'])
def display_signup_form():
    """ Display sign Up page. """

    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    """ Sign up new user and then redirect to homepage. """

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    username = request.form.get('username')
    password = request.form.get('password1')

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    username=username,
                    password=password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = db.session.query(User.user_id).filter_by(username=username).one()[0]
    flash(f'{username} successfully signed up.')
    return redirect('/')

@app.route('/login', methods=['GET'])
def display_login_form():
    """ Display log in page. """

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """ Login the user. """

    username = request.form.get('username')
    session['user_id'] = db.session.query(User.user_id).filter_by(username=username).one()[0]
    flash(f'{username} successfully logged in.')
    return redirect('/')

@app.route('/user_exists', methods=['GET'])
def user_exists():
    """ Determines if username given already exists in the database. """
    username = request.args.get('username')
    if User.query.filter_by(username=username).first() is not None:
        return 'found'
    return 'not found'

@app.route('/validate_login', methods=['POST'])
def validate_login_credentials():
    """ Take username and password and validate them. """

    username = request.form.get('username')
    password = request.form.get('password')

    if User.query.filter_by(username=username, password=password).first() is not None:
        return 'valid'
    return 'not valid'

@app.route('/logout')
def logout():
    """ Logout the current logged in user. """

    user_id = session['user_id']
    username = db.session.query(User.username).filter_by(user_id=user_id).one()[0]
    flash(f'{username} successfully logged out.')
    del session['user_id']

    return redirect('/')

@app.route('/programs')
def display_programs():
    """ Displays progam search page. """

    return render_template('programs.html')


def search_all_programs(search_text, search_type):
    programs_lst_of_tups = []
    if search_type == 'program_name':
        programs_lst_of_tups = db.session.query(
                             Program.program_id,
                             Program.program_name, 
                             Program.address, 
                             Program.city, 
                             Program.state, 
                             Program.zipcode).filter(Program.program_name.like(f'%{search_text}%')).all()
    elif search_type == 'city':
        programs_lst_of_tups = db.session.query(
                             Program.program_id,
                             Program.program_name, 
                             Program.address, 
                             Program.city, 
                             Program.state, 
                             Program.zipcode).filter(Program.city.like(f'%{search_text}%')).all()
    elif search_type == 'state':
        programs_lst_of_tups = db.session.query(
                             Program.program_id,
                             Program.program_name, 
                             Program.address, 
                             Program.city, 
                             Program.state, 
                             Program.zipcode).filter(Program.state.like(f'%{search_text}%')).all()
    elif search_type == 'zipcode':
        programs_lst_of_tups = db.session.query(
                             Program.program_id,
                             Program.program_name, 
                             Program.address, 
                             Program.city, 
                             Program.state, 
                             Program.zipcode).filter(Program.zipcode.like(f'%{search_text}%')).all()
    return programs_lst_of_tups

def search_for_user_favorite_programs(search_text, search_type):
    fav_programs_lst_of_tups = []
    if 'user_id' in session:
        user_id = session['user_id']
        if search_type == 'program_name':
            fav_programs_lst_of_tups = db.session.query(
                                 Program.program_id,
                                 Program.program_name, 
                                 Program.address, 
                                 Program.city, 
                                 Program.state, 
                                 Program.zipcode).join(UserProgram).filter(Program.program_name.like(f'%{search_text}%'),
                                                                           UserProgram.user_id == user_id).all()
        elif search_type == 'city':
            fav_programs_lst_of_tups = db.session.query(
                                 Program.program_id,
                                 Program.program_name, 
                                 Program.address, 
                                 Program.city, 
                                 Program.state, 
                                 Program.zipcode).join(UserProgram).filter(Program.city.like(f'%{search_text}%'),
                                                                           UserProgram.user_id == user_id).all()
        elif search_type == 'state':
            fav_programs_lst_of_tups = db.session.query(
                                 Program.program_id,
                                 Program.program_name, 
                                 Program.address, 
                                 Program.city, 
                                 Program.state, 
                                 Program.zipcode).join(UserProgram).filter(Program.state.like(f'%{search_text}%'),
                                                                           UserProgram.user_id == user_id).all()
        elif search_type == 'zipcode':
            fav_programs_lst_of_tups = db.session.query(
                                 Program.program_id,
                                 Program.program_name, 
                                 Program.address, 
                                 Program.city, 
                                 Program.state, 
                                 Program.zipcode).join(UserProgram).filter(Program.zipcode.like(f'%{search_text}%'),
                                                                           UserProgram.user_id == user_id).all()
    return fav_programs_lst_of_tups

@app.route('/search_programs')
def search_for_programs():

    search_text = request.args.get('search_text')
    search_type = request.args.get('search_type')

    # obtain list of programs that match search
    programs_lst_of_tups = search_all_programs(search_text, search_type)
    # obtain list of all programs that match search and are the current user's favorites
    # this returns an empty list if no user is logged in right now
    fav_programs_lst_of_tups = search_for_user_favorite_programs(search_text, search_type)

    # convert each to a set
    programs_set = set(programs_lst_of_tups)
    fav_programs_set = set(fav_programs_lst_of_tups)

    # perform set subtraction to get programs that are not favorited by the current user
    not_fav_programs_set = programs_set - fav_programs_set

    # create list of dictionaries that will be sent to the frontend
    programs_lst_of_dicts = []

    # add favorites first and mark them as favorite
    for program in fav_programs_set:
        program_dict = {}

        program_dict['program_id'] = program[0]
        program_dict['program_name'] = program[1]
        program_dict['address'] = program[2]
        program_dict['city'] = program[3]
        program_dict['state'] = program[4]
        program_dict['zipcode'] = program[5]
        program_dict['favorite'] = 1

        programs_lst_of_dicts.append(program_dict)

    # next add all the other programs that were not favorited
    for program in not_fav_programs_set:
        program_dict = {}

        program_dict['program_id'] = program[0]
        program_dict['program_name'] = program[1]
        program_dict['address'] = program[2]
        program_dict['city'] = program[3]
        program_dict['state'] = program[4]
        program_dict['zipcode'] = program[5]
        program_dict['favorite'] = 0

        programs_lst_of_dicts.append(program_dict)

    return jsonify(programs_lst_of_dicts)

@app.route('/toggle_favorite') 
def toggle_favorite():
    program_id = request.args.get('program_id')

    if 'user_id' in session:
        user_id = session['user_id']
        favorite_exists = db.session.query(Program).join(UserProgram).filter(UserProgram.user_id==user_id, 
                                                                             Program.program_id==program_id).first()

        if favorite_exists is None:
            # let the user favorite the program
            user_program = UserProgram(user_id = user_id, program_id=program_id)
            db.session.add(user_program)
            db.session.commit()
            return 'favorite'
        else:
            # let the user unfavorite the program
            db.session.query(UserProgram).filter(UserProgram.user_id==user_id, 
                                                 UserProgram.program_id==program_id).delete()
            db.session.commit()
            return 'unfavorite'
    return 'no user logged in'


if __name__ == '__main__':
    # debug must be set to True at the point that DebugToolbarExtension is invoked
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')