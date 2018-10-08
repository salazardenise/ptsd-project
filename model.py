""" Modles and database functions for PTSD Project. """

from flask-sqlalchemy import SQLAlchemy

""" This is the connection to the PostgreSQL database, 
obtained through the Flask-SQLAlchemy helper library. """

db = SQLAlchemy();

##############################################################################
# Model definitions

class User(db.Model):
    """ User of PTSD Project website. """

    pass

class Program(db.Model):
    """ PTSD Program from VA Web service. """

    pass

class UserProgram(db.Model):
    """ Association table between User and Program tables. """

    pass

class Recording(db.Model):
    """ Relaxing recording for Self Care page of PTSD Project website. """

    pass

class UserRecording(db.Model):
    """ Association table between User and Recording tables. """

    pass

class Message(db.Model):
    """ Message Template for a user to send. """

    pass

class UserMessage(db.Model):
    """ Association table between User and Message tables. """
    
    pass
