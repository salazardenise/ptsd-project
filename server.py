""" backend server for PTSD Project app """

# standard python imports
import os
import base64
from email.mime.text import MIMEText
import hashlib
import binascii
from operator import attrgetter
import re

# third party imports
import requests

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for)
# from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Facility, Recording, Message)
from model import (UserFacility, UserRecording, UserMessage)
from model import connect_to_db, db
from twilio.rest import Client

# modules for google oauth
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from apiclient import errors

# salt size for salting passwords when new user signs up
SALT_SIZE = 16

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

app = Flask(__name__)

# app.secret_key is required to use Flask sessions and the debug toolbar
app.secret_key = 'temporary_secret_key'

# set the following so that if an undefined variable is used in Jinja2,
# it doesn't fail silently
app.jinja_env.undefined = StrictUndefined

@app.route('/privacy-policy')
def display_privacy_policy():
    """ Display privacy policy page. """

    return render_template('privacy-policy.html')

def get_random_quote():
    """ Get random quote from healthruwords quote generator API. """

    healthruwords_url = 'https://healthruwords.p.mashape.com/v1/quotes/'
    params = {
        'maxR': 1,
        'size': 'medium',
        't': 'Hope'
    }
    headers = {
        'X-Mashape-Key': os.environ['HEALTHRUWORDS_API_KEY'],
        'Accept': 'application/json',
        'User-Agent': ''
    }
    quote_results = requests.get(healthruwords_url,
                                 params=params,
                                 headers=headers)

    if quote_results.status_code == 200 and not quote_results.json()[0]['media'].endswith('height'):
        quote = quote_results.json()[0]
    else:
        # default quote if call to API fails
        quote = {
            'media': 'http://healthruwords.com/wp-content/uploads/2016/09/Healthruwords.com_-_Inspirational_Images_-_Imagination-over-Knowledge-300x300.jpg',
            'author': 'Roxana Jones'
        }
    return quote

@app.route('/')
def index():
    """ Display homepage. """
    quote = get_random_quote()

    return render_template('homepage.html', quote=quote)

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
    password_plain = request.form.get('password1')
    salt = binascii.hexlify(os.urandom(SALT_SIZE))
    password_hash = hashlib.sha256(password_plain.encode('utf-8') + salt).hexdigest()

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    username=username,
                    password=password_hash,
                    salt=salt.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = db.session.query(User.user_id).filter_by(username=username).one()[0]
    flash(f'{username} successfully signed up.')
    return redirect('/')

@app.route('/login', methods=['GET'])
def display_login_form():
    """ Display log in page. """

    return render_template('login.html')

@app.route('/validate_signup', methods=['GET'])
def user_exists():
    """ Determines if username given already exists in the database. """

    if 'username' not in request.args:
        return jsonify({'username_found': False})

    username = request.args.get('username')
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'username_found': True})
    return jsonify({'username_found': False})

@app.route('/login', methods=['POST'])
def validate_login_credentials():
    """ Take username and password and validate them. """

    username = request.form.get('username')
    password_entered_plain = request.form.get('password')

    result = {}
    # Does username exist?
    user = User.query.filter_by(username=username).first()
    if user is None:
        result['username_found'] = False
        result['valid_login'] = None
        return jsonify(result)

    # If yes, does password match username?
    result['username_found'] = True
    salt = user.salt.encode('utf-8')

    password_entered_hash = hashlib.sha256(password_entered_plain.encode('utf-8') + salt).hexdigest()
    password_db_hash = user.password

    if password_db_hash == password_entered_hash:
        result['valid_login'] = True
        # log user in by assing their id to the session
        session['user_id'] = user.user_id
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
    if 'credentials' in session:
        # revoke and clear credenitals:
        # credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        # revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
        #                        params={'token': credentials.token},
        #                       headers = {'content-type': 'application/x-www-form-urlencoded'})

        # status_code = getattr(revoke, 'status_code')
        # if status_code == 200:
        #     print('\n\nCredentials successfully revoked.')
        # else:
        #     print('\n\nAn error occurred.')
        del session['credentials']

    return redirect('/')

@app.route('/user_profile', methods=['GET'])
def display_user_profile():
    """ Display user profile page. """
    if 'user_id' in session:
        user_id = session.get('user_id', None)
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('user_profile.html', user=user)

    flash('Sign Up or Log In in order to see your user profile.')
    return redirect('/')

@app.route('/user_profile', methods=['POST'])
def edit_user_profile():
    """ Save any changes the user made to their profile. """

    if 'user_id' in session:
        user_id = session.get('user_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        if phone == '000-000-0000':
            phone = None

        updates = {'first_name': first_name,
                   'last_name': last_name,
                   'email': email,
                   'phone': phone}
        db.session.query(User).filter(User.user_id == user_id).update(updates)
        db.session.commit()

        flash('User profile saved.')
        return redirect('/')

    flash('Sign Up or Log In in order to see your user profile.')
    return redirect('/')

@app.route('/change_password', methods=['POST'])
def change_password():
    """ Changes user password and redirects to home. """

    current_password_plain = request.form.get('current_password')
    new_password_plain = request.form.get('new_password1')

    result = {}
    # Get user
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()

    # Does current password match username?
    current_salt = user.salt.encode('utf-8')
    current_password_hash = hashlib.sha256(current_password_plain.encode('utf-8') + current_salt).hexdigest()
    current_password_db_hash = user.password

    if current_password_db_hash == current_password_hash:
        result['valid_password_change'] = True
        # password matches! now change the password
        new_salt = binascii.hexlify(os.urandom(SALT_SIZE))
        new_password_hash = hashlib.sha256(new_password_plain.encode('utf-8') + new_salt).hexdigest()
        updates = {'password': new_password_hash,
                   'salt': new_salt.decode('utf-8')}
        db.session.query(User).filter(User.user_id == user_id).update(updates)
        db.session.commit()
    else:
        result['valid_password_change'] = False

    return jsonify(result)


@app.route('/programs')
def display_programs():
    """ Displays progam search page. """

    return render_template('programs.html')

@app.route('/programs.json')
def search_for_programs():
    """ Get list of facilities in json format given search text and type. """

    search_text = request.args.get('search_text')
    search_type = request.args.get('search_type')

    user_id = session.get('user_id', None)
    sub = db.session.query(UserFacility).filter(UserFacility.user_id == user_id).subquery()
    base_query = db.session.query(Facility, sub.c.user_id).outerjoin(sub)

    if search_type == 'fac_name':
        base_with_filter = base_query.filter(Facility.fac_name.like(f'%{search_text}%'))
    elif search_type == 'city':
        base_with_filter = base_query.filter(Facility.city.like(f'%{search_text}%'))
    elif search_type == 'state':
        base_with_filter = base_query.filter(Facility.state.like(f'%{search_text}%'))
    elif search_type == 'zipcode':
        base_with_filter = base_query.filter(Facility.zipcode.like(f'%{search_text}%'))
    else:
        return jsonify([])

    facilities = base_with_filter.order_by(sub.c.user_id, Facility.fac_name).all()
    # facilities is a list of tuples
    # each facility in facilities is (<Facility>, user_id)

    lst_of_facilities = []
    for facility in facilities:
        facility_dict = {}

        facility_dict['fac_id'] = facility[0].fac_id
        facility_dict['fac_name'] = facility[0].fac_name
        facility_dict['address'] = facility[0].address
        facility_dict['city'] = facility[0].city
        facility_dict['state'] = facility[0].state
        facility_dict['zipcode'] = facility[0].zipcode
        if facility[1] is not None:
            facility_dict['favorite'] = 1
        else:
            facility_dict['favorite'] = 0

        lst_of_facilities.append(facility_dict)

    return jsonify(lst_of_facilities)

@app.route('/programs_by_facility.json')
def return_programs_of_facility():
    """ Given a facility id return the programs of the facility in JSON format. """

    fac_id = request.args.get('fac_id')
    facility = Facility.query.filter_by(fac_id=fac_id).one()

    lst_of_programs = []
    programs_sorted = sorted(list(facility.programs), key=attrgetter('program_name'))
    for program in programs_sorted:
        program_dict = {}

        program_dict['program_id'] = program.program_id
        program_dict['program_name'] = program.program_name

        lst_of_programs.append(program_dict)

    return jsonify(lst_of_programs)

@app.route('/toggle_favorite_facility')
def toggle_favorite_program():
    """ Given a facility id, toggle favoritig it as long as user is logged in. """

    fac_id = request.args.get('fac_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Facility).join(UserFacility).filter(UserFacility.user_id == user_id,
                                                                               UserFacility.fac_id == fac_id).first()

        if favorite_exists is None:
            # let the user favorite the program
            user_facility = UserFacility(user_id=user_id, fac_id=fac_id)
            db.session.add(user_facility)
            db.session.commit()
            results['favorite'] = True
        else:
            # let the user unfavorite the program
            db.session.query(UserFacility).filter(UserFacility.user_id == user_id,
                                                  UserFacility.fac_id == fac_id).delete()
            db.session.commit()
            results['favorite'] = False
    else:
        results['user_logged_in'] = False
        results['favorite'] = None

    return jsonify(results)

@app.route('/toggle_favorite_recording')
def toggle_favorite_recording():
    """ Given a recording id, toggle favoritig it as long as user is logged in. """

    recording_id = request.args.get('recording_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Recording).join(UserRecording).filter(UserRecording.user_id == user_id,
                                                                                 Recording.recording_id == recording_id).first()

        if favorite_exists is None:
            # let the user favorite the recording
            user_recording = UserRecording(user_id=user_id, recording_id=recording_id)
            db.session.add(user_recording)
            db.session.commit()
            results['favorite'] = True
        else:
            # the the user unfavorite the recording
            db.session.query(UserRecording).filter(UserRecording.user_id == user_id,
                                                   UserRecording.recording_id == recording_id).delete()
            db.session.commit()
            results['favorite'] = False
    else:
        results['user_logged_in'] = False
        results['favorite'] = None

    return jsonify(results)

@app.route('/toggle_favorite_message')
def toggle_favorite_message():
    """ Given a message id, toggle favoritig it as long as user is logged in. """

    message_id = request.args.get('message_id')
    results = {}

    if 'user_id' in session:
        user_id = session['user_id']
        results['user_logged_in'] = True
        favorite_exists = db.session.query(Message).join(UserMessage).filter(UserMessage.user_id == user_id,
                                                                             Message.message_id == message_id).first()

        if favorite_exists is None:
            # let the user favorite the message
            user_message = UserMessage(user_id=user_id, message_id=message_id)
            db.session.add(user_message)
            db.session.commit()
            results['favorite'] = True
        else:
            # the the user unfavorite the message
            db.session.query(UserMessage).filter(UserMessage.user_id == user_id,
                                                 UserMessage.message_id == message_id).delete()
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

@app.route('/store_message_id')
def store_message_id():
    """ Stores message_id to the session. """
    message_id = request.args.get('message_id')
    session['message_id'] = message_id
    return jsonify({'added': True})
    # return redirect('/email_message')

@app.route('/email_message', methods=['GET'])
def display_email_message():
    """ Display email message page.

    This route should only be called when a user is logged in.
    i.e. A user that is not logged in should not be able to send an email message.
    """

    # check if user in session
    if 'user_id' not in session:
        flash('Sign Up or Log In to enable sending email message templates.')
        return redirect('/')

    # check if message_id in session
    if 'message_id' not in session:
        flash('Access sending an email message by going to the /messages page first.')
        return redirect('/')

    # check if user authorized app, if not, redirect to authorize route
    if 'credentials' not in session:
        return redirect('/authorize')

    user_id = session['user_id']
    user = User.query.filter(User.user_id == user_id).one()

    message_id = session.get('message_id')
    message = Message.query.filter(Message.message_id == message_id).one()

    return render_template('email_message.html', message=message, user=user)

def create_email_message_content(to_name, body_message, from_first_name, from_last_name):
    """ Create content for email message. """

    content_message = 'Dear'
    if to_name:
        content_message += ' ' + to_name
    content_message += ', \n\n'
    content_message += body_message + '\n\n'
    content_message += 'Best, ' + from_first_name + ' ' + from_last_name
    return content_message

@app.route('/email_message', methods=['POST'])
def process_email_message():
    """ Process sending an email message. """

    # extract message info
    from_first_name = request.form.get('from_first_name')
    from_last_name = request.form.get('from_last_name')
    to_name = request.form.get('to_name')
    body_message = request.form.get('body_message')
    # create content for message
    content_message = create_text_message_content(to_name=to_name,
                                                  body_message=body_message,
                                                  from_first_name=from_first_name,
                                                  from_last_name=from_last_name)

    # extract to_email and subject
    to_email = request.form.get('to_email')
    if re.match(r'[^@]+@[^@]+\.[^@]+', to_email) is False:
        flash('To Email entered was invalid.')
        redirect('/')
    subject = request.form.get('subject')

    # create message for sending
    user_id = session['user_id']
    user = User.query.filter(User.user_id == user_id).one()
    message = create_message(user.email, to_email, subject, content_message)

    # send message
    message_status = load_message_and_send(message)
    # message_status['labelIds'] is a list of strings
    if message_status is None:
        flash('Email message was not sent. Make sure you have a gmail address in your user profile.')
    elif 'SENT' in message_status['labelIds']:
        flash('Email message was sent.')
    else:
        flash('Email message was not sent.')
    return redirect('/')

def load_message_and_send(created_message):
    """ This functions loads the created message and sends it using google gmail API. """

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    send_service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).one()

    message_status = send_message(send_service, user.email, created_message)
    # message_status = send_message(send_service, 'me', created_message)
    # message_status is None if invalid user id specified in request/Delegation denied

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return message_status

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        return message
    # except googleapiclient.errors.HttpError as err:
    except errors.HttpError as error:
        print('\n\nAn error occurred:', error)

@app.route('/authorize')
def authorize():
    """ authorize route sends user to google oauth page """

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = 'https://findingpeaceptsd.com/oauth2callback'

    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).one()

    # Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        #which email is trying to login?
        login_hint=user.email,
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    # Redirect to Google's OAuth 2.0 server
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """ The route google oauth goes to when user authorizes this app. """

    if 'error' in request.args:
        print('\n Error occured')
        flash('You must approve app access to send an email.')
        return redirect('/')

    # if 'error' in request.args:
    #     if request.args.get('error') == 'access_denied':
    #         return 'You denied access.'
    #     return 'Error encountered.'

    # Specify the state when creating the flow in the callback so that it can be
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = 'https://findingpeaceptsd.com/oauth2callback'

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    # now turn those parameters into a token.
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('display_email_message'))

def credentials_to_dict(credentials):
    """ Takes credentials and creates dictionary of each of its attributes """

    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

@app.route('/text_message', methods=["GET"])
def display_text_message():
    """ Display text message page.

    This route should only be called when a user is logged in.
    i.e. A user that is not logged in should not be able to send a text message.
    """
    if 'message_id' not in request.args:
        flash('Access sending a text message by going to the /messages page first.')
        return redirect('/')

    if 'user_id' not in session:
        flash('Sign Up or Log In to enable sending text message templates.')
        return redirect('/')

    message_id = request.args.get('message_id')
    message = Message.query.filter(Message.message_id == message_id).one()

    user_id = session['user_id']
    user = User.query.filter(User.user_id == user_id).one()

    return render_template('text_message.html',
                           message=message,
                           user=user)

@app.route('/validate_logged_in')
def validate_logged_in():
    """" validates if a user is logged in or not. """
    if 'user_id' in session:
        results = {'user_logged_in': True}
    else:
        results = {'user_logged_in': False}
    return jsonify(results)

def create_text_message_content(to_name, body_message, from_first_name, from_last_name):
    """ Create text message content. """

    content_message = 'Hi'
    if to_name:
        content_message += ' ' + to_name
    content_message += ', \n\n'
    content_message += body_message + '\n\n'
    content_message += 'Best, ' + from_first_name + ' ' + from_last_name
    content_message += '\n\n'
    content_message += 'This message was sent from the Finding Peace website.'
    return content_message

def send_text_message(from_, body, to):
    """ Send a text message. """

    # Twilio credentials
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(from_=from_,
                                     body=body,
                                     to=to)
    return message

@app.route('/text_message', methods=["POST"])
def process_text_message():
    """ Process sending a text message. """

    # extract message info
    from_first_name = request.form.get('from_first_name')
    from_last_name = request.form.get('from_last_name')
    to_name = request.form.get('to_name')
    body_message = request.form.get('body_message')
    # create message
    content_message = create_text_message_content(to_name=to_name,
                                                  body_message=body_message,
                                                  from_first_name=from_first_name,
                                                  from_last_name=from_last_name)

    # extract phone number ensure it is valid
    phone_raw = request.form.get('phone')
    if re.match(r'\d{3}[\-]\d{3}[\-]\d{4}', phone_raw) is False:
        flash('Phone number entered was invalid.')
        return redirect('/')
    phone_list = phone_raw.split('-')
    phone_without_country_code = ''.join(phone_list)
    phone = '+1' + phone_without_country_code

    # phone numbers to use
    from_ = os.environ['TWILIO_FROM_NUMBER']
    to_ = phone

    # send text message
    message = send_text_message(from_, content_message, to_)

    if message.error_code is not None:
        flash('Error sending message.')
    else:
        flash(f'Message sent to {to_name}.')
    return redirect('/')

if __name__ == '__main__':
    # # debug must be set to True at the point that DebugToolbarExtension is invoked
    # app.debug = True
    # # make sure templates, etc. are not cached in debug mode
    # app.jinja_env.auto_reload = app.debug
    # DebugToolbarExtension(app)
    connect_to_db(app)
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(port=5000, host='0.0.0.0')
    #app.run(port=5000)
