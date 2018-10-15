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

@app.route('/validate_signup', methods=['GET'])
def user_exists():
    """ Determines if username given already exists in the database. """
    username = request.args.get('username')
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'username_found': True})
    return jsonify({'username_found': False})

@app.route('/validate_login', methods=['POST'])
def validate_login_credentials():
    """ Take username and password and validate them. """

    username = request.form.get('username')
    password = request.form.get('password')

    result = {}
    # Does username exist?
    if User.query.filter_by(username=username).first() is None:
        result['username_found'] = False
        result['valid_login'] = None
        return jsonify(result)
    
    # If yes, does password match username?
    result['username_found'] = True
    if User.query.filter_by(username=username, password=password).first() is not None:
        result['valid_login'] = True
    else:
        result['valid_login'] = False

    return jsonify(result)

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
    baseQuery = db.session.query(
                             Program.program_id,
                             Program.program_name, 
                             Program.address, 
                             Program.city, 
                             Program.state, 
                             Program.zipcode)

    if search_type == 'program_name':
        base_with_filter = baseQuery.filter(Program.program_name.like(f'%{search_text}%'))
    elif search_type == 'city':
        base_with_filter = baseQuery.filter(Program.city.like(f'%{search_text}%'))
    elif search_type == 'state':
        base_with_filter = baseQuery.filter(Program.state.like(f'%{search_text}%'))
    elif search_type == 'zipcode':
        base_with_filter = baseQuery.filter(Program.zipcode.like(f'%{search_text}%'))
    else:
        return []

    return base_with_filter.all()

def search_for_user_favorite_programs(search_text, search_type):
    if 'user_id' in session:
        
        user_id = session['user_id']

        baseQuery = db.session.query(
                                 Program.program_id,
                                 Program.program_name, 
                                 Program.address, 
                                 Program.city, 
                                 Program.state, 
                                 Program.zipcode).join(UserProgram)

        if search_type == 'program_name':
            base_with_filter = baseQuery.filter(Program.program_name.like(f'%{search_text}%'),
                                                UserProgram.user_id == user_id)
        elif search_type == 'city':
            base_with_filter = baseQuery.filter(Program.city.like(f'%{search_text}%'),
                                                UserProgram.user_id == user_id)
        elif search_type == 'state':
            base_with_filter = baseQuery.filter(Program.state.like(f'%{search_text}%'),
                                                UserProgram.user_id == user_id)
        elif search_type == 'zipcode':
            base_with_filter = baseQuery.filter(Program.zipcode.like(f'%{search_text}%'),
                                                UserProgram.user_id == user_id)
        else:
            # no appropriate search type was chosen
            return []
    else:
        # no user is logged in and therefore there are no favorites
        return []
    return base_with_filter.all()

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

@app.route('/toggle_favorite_program') 
def toggle_favorite_program():
    program_id = request.args.get('program_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Program).join(UserProgram).filter(UserProgram.user_id==user_id, 
                                                                             Program.program_id==program_id).first()

        if favorite_exists is None:
            # let the user favorite the program
            user_program = UserProgram(user_id = user_id, program_id=program_id)
            db.session.add(user_program)
            db.session.commit()
            results['favorite'] = True
        else:
            # let the user unfavorite the program
            db.session.query(UserProgram).filter(UserProgram.user_id==user_id, 
                                                 UserProgram.program_id==program_id).delete()
            db.session.commit()
            results['favorite'] = False
    else:
        results['user_logged_in'] = False
        results['favorite'] = None
    
    return jsonify(results)

@app.route('/toggle_favorite_recording')
def toggle_favorite_recording():

    recording_id = request.args.get('recording_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Recording).join(UserRecording).filter(UserRecording.user_id==user_id,
                                                                                 Recording.recording_id==recording_id).first()

        if favorite_exists is None:
            # let the user favorite the recording
            user_recording = UserRecording(user_id=user_id, recording_id=recording_id)
            db.session.add(user_recording)
            db.session.commit()
            results['favorite'] = True
        else:
            # the the user unfavorite the recording
            db.session.query(UserRecording).filter(UserRecording.user_id==user_id,
                                                   UserRecording.recording_id==recording_id).delete()
            db.session.commit()
            results['favorite'] = False
    else:
        results['user_logged_in'] = False
        results['favorite'] = None
    
    return jsonify(results)

@app.route('/toggle_favorite_message')
def toggle_favorite_message():

    message_id = request.args.get('message_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Message).join(UserMessage).filter(UserMessage.user_id==user_id,
                                                                             Message.message_id==message_id).first()

        if favorite_exists is None:
            # let the user favorite the message
            user_message = UserMessage(user_id=user_id, message_id=message_id)
            db.session.add(user_message)
            db.session.commit()
            results['favorite'] = True
        else:
            # the the user unfavorite the message
            db.session.query(UserMessage).filter(UserMessage.user_id==user_id,
                                                 UserMessage.message_id==message_id).delete()
            db.session.commit()
            results['favorite'] = False
    else:
        results['user_logged_in'] = False
        results['favorite'] = None
    
    return jsonify(results)

@app.route('/recordings')
def display_recordings():
    """ Display recordings page. """

    favorite_recordings = []
    # get user's favorite recordings
    if 'user_id' in session:
        user_id = session['user_id']
        favorite_recordings = db.session.query(Recording.recording_id,
                                               Recording.name,
                                               Recording.description,
                                               Recording.file_path).join(UserRecording).filter(UserRecording.user_id==user_id).all()
    
    # get all recordings
    recordings = db.session.query(Recording.recording_id,
                                  Recording.name,
                                  Recording.description,
                                  Recording.file_path).all()

    # convert each to a set
    favorite_recordings_set = set(favorite_recordings)
    recordings_set = set(recordings)

    # perform set subtraction to get recordings that are not favorited by the current user
    recordings_not_fav_set = recordings_set - favorite_recordings_set

    # create list of dictionaries for each recording
    recording_lst_of_dicts = []

    # add favorites first and mark them as favorite
    for recording in favorite_recordings_set:
        recording_dict = {}

        recording_dict['recording_id'] = recording[0]
        recording_dict['name'] = recording[1]
        recording_dict['description'] = recording[2]
        recording_dict['file_path'] = recording[3]
        recording_dict['favorite'] = 1

        recording_lst_of_dicts.append(recording_dict)

    # next add all the other programs that were not favorited
    for recording in recordings_not_fav_set:
        recording_dict = {}

        recording_dict['recording_id'] = recording[0]
        recording_dict['name'] = recording[1]
        recording_dict['description'] = recording[2]
        recording_dict['file_path'] = recording[3]
        recording_dict['favorite'] = 0

        recording_lst_of_dicts.append(recording_dict)

    return render_template('recordings.html', recording_lst_of_dicts=recording_lst_of_dicts)

@app.route('/messages')
def display_messages():
    """ Display messages page. """

    user_id = session.get('user_id', None)
    sub = db.session.query(UserMessage).filter(UserMessage.user_id == user_id).subquery()
    messages = db.session.query(Message, sub.c.user_id).outerjoin(sub).order_by(sub.c.user_id, Message.message_id).all()
    # messages is a list of tuples
    # each message in messages is (<Message>, user_id)
        
    return render_template('messages.html', messages=messages)




if __name__ == '__main__':
    # debug must be set to True at the point that DebugToolbarExtension is invoked
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')