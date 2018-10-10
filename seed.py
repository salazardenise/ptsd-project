from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db 
from server import app

def load_dummy_data():
    print('User')
    denise = User(username='denisecodes', password='Python', 
                  first_name='Denise', last_name='Codes', email='denise@codes.com')
    roy = User(username='roycodes', password='Python',
                  first_name='Roy', last_name='Codes', email='roy@codes.com')
    leo = User(username="leocodes", password="Java",
                  first_name='Leo', last_name='Codes', email='leo@codes.com')
    turing = User(username='turingcodes', password='JavaScript',
                  first_name='Turing', last_name='Codes', email='turing@codes.com')

    print('Program')
    angels = Program(address='100 A St', city='CityOfAngels', 
                        fac_id=1, fac_name='fac_name', program_name='angels',
                        state='CA', zipcode=10000)
    devils = Program(address='100 B St', city='CityOfDevils', 
                        fac_id=1, fac_name='fac_name', program_name='devils',
                        state='CA', zipcode=20000)
    wizards = Program(address='100 C St', city='CityOfWizards', 
                        fac_id=1, fac_name='fac_name', program_name='wizards',
                        state='CA', zipcode=30000)
    denise.programs.append(angels)
    denise.programs.append(devils)
    denise.programs.append(wizards)
    roy.programs.append(devils)
    roy.programs.append(wizards)

    print('Recording')
    ocean = Recording(name='Ocean', description='Ocean sounds', file_path='/static/ocean')
    wind = Recording(name='Wind', description='Wind sounds', file_path='/static/wind')
    park = Recording(name='Park', description='Park sounds', file_path='/static/park')
    denise.recordings.append(ocean)
    denise.recordings.append(wind)
    denise.recordings.append(park)
    roy.recordings.append(wind)
    roy.recordings.append(park)

    print('Message')
    family = Message(message_type='Family', message='I am not feeling well. I will contact you when I start feeling better.')
    boss = Message(message_type='Co-worker', message='I am out sick today. Please message me if there are any immediate deliverables for today.')
    friend = Message(message_type='Friend', message='I really wanted to see you but I cannot visit with you today. Will get in touch when I am feeling better.')
    denise.messages.append(family)
    denise.messages.append(boss)
    denise.messages.append(friend)
    roy.messages.append(boss)
    roy.messages.append(friend)

    db.session.add_all([denise, roy, leo, turing])
    db.session.commit()


if __name__ == '__main__':
    connect_to_db(app)

    # create the tables
    db.create_all()

    # import dummy data
    load_dummy_data()

