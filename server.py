""" PTSD Project """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db
from twilio.rest import Client
import os

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

@app.route('/programs.json')
def search_for_programs():

    search_text = request.args.get('search_text')
    search_type = request.args.get('search_type')

    user_id = session.get('user_id', None)
    sub = db.session.query(UserProgram).filter(UserProgram.user_id == user_id).subquery()
    baseQuery = db.session.query(Program, sub.c.user_id).outerjoin(sub)

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

    programs = base_with_filter.order_by(sub.c.user_id, Program.program_id).all()
    # programs is a list of tuples
    # each program in programs is (<Program>, user_id)
    
    lst_of_programs = []
    for program in programs:
        program_dict = {}

        program_dict['program_id'] = program[0].program_id
        program_dict['program_name'] = program[0].program_name
        program_dict['address'] = program[0].address
        program_dict['city'] = program[0].city
        program_dict['state'] = program[0].state
        program_dict['zipcode'] = program[0].zipcode
        if program[1] != None:
            program_dict['favorite'] = 1
        else:
            program_dict['favorite'] = 0

        lst_of_programs.append(program_dict)

    return jsonify(lst_of_programs)

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

    user_id = session.get('user_id', None)
    sub = db.session.query(UserRecording).filter(UserRecording.user_id == user_id).subquery()
    recordings = db.session.query(Recording, sub.c.user_id).outerjoin(sub).order_by(sub.c.user_id, Recording.recording_id).all()
    # recordings is a list of tuples
    # each recording in recordings is (<Recording>, user_id)
        
    return render_template('recordings.html', recordings=recordings)

@app.route('/messages')
def display_messages():
    """ Display messages page. """

    user_id = session.get('user_id', None)
    sub = db.session.query(UserMessage).filter(UserMessage.user_id == user_id).subquery()
    messages = db.session.query(Message, sub.c.user_id).outerjoin(sub).order_by(sub.c.user_id, Message.message_id).all()
    # messages is a list of tuples
    # each message in messages is (<Message>, user_id)
        
    return render_template('messages.html', messages=messages)

@app.route('/email_message')
def display_email_message():
    return "email message page"

@app.route('/text_message', methods=["GET"])
def display_text_message():
    """ Display text message page. 

    This route should only be called when a user is logged in.
    i.e. A user that is not logged in should not be able to send a text message.
    """

    message_id = request.args.get('message_id')
    message = Message.query.filter(Message.message_id == message_id).one()

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter(User.user_id == user_id).one()

        return render_template('text_message.html', 
                               message=message,
                               user=user)
    else:
        flash('Sign Up or Log In to enable sending text message templates.')
        return redirect('/')

def send_text_message(from_, body, to):
    """ Send a text message. """

    # Twilio credentials
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token) 

    message = client.messages.create( 
                              from_=from_,
                              body=body,
                              to=to)

@app.route('/text_message', methods=["POST"])
def process_text_message():
    """ Process sending a text message. """

    # message info
    from_first_name = request.form.get('from_first_name')
    from_last_name = request.form.get('from_last_name')
    to_name = request.form.get('to_name')
    body_message = request.form.get('body_message')
    phone_raw = request.form.get('phone')
    phone_list = phone_raw.split('-')
    phone = ''.join(phone_list)
    print(phone)

    # create message
    content_message = 'Hi'
    if len(to_name) != 0:
        content_message += ' ' + to_name
    content_message += ', \n\n'
    content_message += body_message + '\n\n'
    content_message += 'Best, ' + from_first_name + ' ' + from_last_name

    # phone numbers to use
    # FOR DEMO PURPOSES, 
    # TWILIO TRAIL ACCOUNT ALLOWS SENDING TEXTS ONLY TO MY PHONE NUMBER
    from_=os.environ['TWILIO_FROM_NUMBER']
    to=os.environ['TWILIO_TO_NUMBER']
    send_text_message(from_, content_message, to)

    flash(f'message sent to {to_name}')
    return redirect('/')

if __name__ == '__main__':
    # debug must be set to True at the point that DebugToolbarExtension is invoked
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')