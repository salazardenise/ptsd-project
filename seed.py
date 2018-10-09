from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db 
from server import app

def load_dummy_users():
    """ Load dummy users. """

    print('User')
    user_1 = User(username='denisecodes', password='Python', 
                  first_name='Denise', last_name='Codes', email='denise@codes.com')
    user_2 = User(username='roycodes', password='Python',
                  first_name='Roy', last_name='Codes', email='roy@codes.com')
    user_3 = User(username="leocodes", password="Java",
                  first_name='Leo', last_name='Codes', email='leo@codes.com')
    user_4 = User(username='turingcodes', password='JavaScript',
                  first_name='Turing', last_name='Codes', email='turing@codes.com')
    db.session.add_all([user_1, user_2, user_3, user_3])
    db.session.commit()

def load_dummy_programs():
    """ Load dummy programs. """

    print('Program')
    program_1 = Program(address='100 A St', city='CityOfAngels', 
                        fac_id=1, fac_name='fac_name', program_name='program_1',
                        state='CA', zipcode=10000)
    program_2 = Program(address='100 B St', city='CityOfDevils', 
                        fac_id=1, fac_name='fac_name', program_name='program_2',
                        state='CA', zipcode=20000)
    program_3 = Program(address='100 C St', city='CityOfWizards', 
                        fac_id=1, fac_name='fac_name', program_name='program_3',
                        state='CA', zipcode=30000)
    db.session.add_all([program_1, program_2, program_3])
    db.session.commit()

def load_dummy_users_progams():
    """ Load dummy users favoriting programs. """

    print('UserProgram')
    user_program_1 = UserProgram(user_id=1, program_id=1)
    user_program_2 = UserProgram(user_id=1, program_id=2)
    user_program_3 = UserProgram(user_id=1, program_id=3)
    user_program_4 = UserProgram(user_id=2, program_id=2)
    user_program_5 = UserProgram(user_id=2, program_id=3)
    db.session.add_all([user_program_1, user_program_2, user_program_3, user_program_4, user_program_5])
    db.session.commit()

def load_dummy_recordings():
    """ Load dummy recordings. """

    print('Recording')
    recording_1 = Recording(name='Ocean', description='Ocean sounds', file_path='/static/ocean')
    recording_2 = Recording(name='Wind', description='Wind sounds', file_path='/static/wind')
    recording_3 = Recording(name='Park', description='Park sounds', file_path='/static/park')
    db.session.add_all([recording_1, recording_2, recording_3])
    db.session.commit()

def load_dummy_users_recordings():
    """ Load dummy users favoriting recordings. """

    print('UserRecording')
    user_recording_1 = UserRecording(user_id=1, recording_id=1)
    user_recording_2 = UserRecording(user_id=1, recording_id=2)
    user_recording_3 = UserRecording(user_id=1, recording_id=3)
    user_recording_4 = UserRecording(user_id=2, recording_id=2)
    user_recording_5 = UserRecording(user_id=2, recording_id=3)
    db.session.add_all([user_recording_1, user_recording_2, user_recording_3, user_recording_4, user_recording_5])
    db.session.commit()

def load_dummy_messages():
    """ Load dummy messages. """

    print("Message")
    message_1 = Message(message_type='Family', message='I am not feeling well. I will contact you when I start feeling better.')
    message_2 = Message(message_type='Co-worker', message='I am out sick today. Please message me if there are any immediate deliverables for today.')
    message_3 = Message(message_type='Friend', message='I really wanted to see you but I cannot visit with you today. Will get in touch when I am feeling better.')
    db.session.add_all([message_1, message_2, message_3])
    db.session.commit()

def load_dummy_users_messages():
    """ Load dummy users favorting messages. """

    print('UserMessage')
    user_message_1 = UserMessage(user_id=1, message_id=1)
    user_message_2 = UserMessage(user_id=1, message_id=2)
    user_message_3 = UserMessage(user_id=1, message_id=3)
    user_message_4 = UserMessage(user_id=2, message_id=2)
    user_message_5 = UserMessage(user_id=2, message_id=3)
    db.session.add_all([user_message_1, user_message_2, user_message_3, user_message_4, user_message_5])
    db.session.commit()

if __name__ == '__main__':
    connect_to_db(app)

    # create the tables
    db.create_all()

    # import dummy data
    load_dummy_users()
    load_dummy_programs()
    load_dummy_users_progams()
    load_dummy_recordings()
    load_dummy_users_recordings()
    load_dummy_messages()
    load_dummy_users_messages()


