""" Modles and database functions for PTSD Project. """

from flask_sqlalchemy import SQLAlchemy

""" This is the connection to the PostgreSQL database, 
obtained through the Flask-SQLAlchemy helper library. """

db = SQLAlchemy();

##############################################################################
# Model definitions

class User(db.Model):
    """ User of PTSD Project website. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(100),
                         nullable=False)
    password = db.Column(db.String(100),
                         nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    programs = db.relationship('Program',
                                secondary='users_programs')
    recordings = db.relationship('Recording',
                                 secondary='users_recordings')
    messages = db.relationship('Message',
                                secondary='users_messages')

    def __repr__(self):
        return f'<User user_id:{self.user_id} username:{self.username}>'

class Program(db.Model):
    """ PTSD Program from VA Web service. """

    __tablename__ = 'programs'

    program_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    fac_id = db.Column(db.Integer, nullable=False)
    fac_name = db.Column(db.String(500), nullable=False)
    program_name = db.Column(db.String(500), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)

    users = db.relationship('User', secondary='users_programs')

    def __repr__(self):
        return f'<Program program_id:{self.program_id} program_name:{self.program_name}>'

class UserProgram(db.Model):
    """ Association table between User and Program tables. """

    __tablename__ = 'users_programs'

    userprogram_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    program_id = db.Column(db.Integer,
                           db.ForeignKey('programs.program_id'),
                           nullable=False)

    def __repr__(self):
        return f'<UserProgram userprogram_id:{self.userprogram_id} user_id:{self.user_id} program_id:{self.program_id}>'

class Recording(db.Model):
    """ Relaxing recording for Self Care page of PTSD Project website. """

    __tablename__ = 'recordings'

    recording_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)

    users = db.relationship('User', secondary='users_recordings')

    def __repr__(self):
        return f'<Recording recording_id:{self.recording_id} name:{self.name}>'

class UserRecording(db.Model):
    """ Association table between User and Recording tables. """

    __tablename__ = 'users_recordings'

    userrecording_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    recording_id = db.Column(db.Integer,
                             db.ForeignKey('recordings.recording_id'),
                             nullable=False)

    def __repr__(self):
        return f'<UserRecording userrecording_id:{self.userrecording_id} user_id:{self.user_id} recording_id:{self.recording_id}>'

class Message(db.Model):
    """ Message Template for a user to send. """

    __tablename__ = 'messages'

    message_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    message_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    users = db.relationship('User', secondary='users_messages')

    def __repr__(self):
        return f'<Message message_id:{self.message_id} message_type:{self.message_type}>'

class UserMessage(db.Model):
    """ Association table between User and Message tables. """

    __tablename__ = 'users_messages'

    usermessage_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    message_id = db.Column(db.Integer,
                             db.ForeignKey('messages.message_id'),
                             nullable=False)

    def __repr__(self):
        return f'<UserMessage usermessage_id:{self.usermessage_id} user_id:{self.user_id} message_id:{self.message_id}>'

##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///ptsd"):
    """ Connect the database to the Flask app. """

    # Configure to use a PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    """ As a convenience, if we run this module interactively,
    this will allow the user to work with the database directly. """

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
