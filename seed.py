from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db 
from server import app
from zeep import Client, helpers
import os

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

def load_programs():
    license = os.environ['VA_LICENSE']

    client = Client('https://www.va.gov/webservices/PTSD/ptsd.cfc?wsdl')

    output = client.service.PTSD_Program_Locator_query(license)

    order = output[1]['value']['_value_1']
    status = output[2]['value']['_value_1']
    matches = output[3]['value']['_value_1']

    columns = output[0]['value']['columnList']
    data = output[0]['value']['data']

    for program_dict in data:
        row_data = program_dict['_value_1']

        fac_id = row_data[0]['_value_1']
        fac_name = row_data[1]['_value_1']
        address = row_data[2]['_value_1']
        city = row_data[3]['_value_1']
        state = row_data[4]['_value_1']
        zipcode = row_data[5]['_value_1']
        program_name = row_data[6]['_value_1']

        program = Program(fac_id=fac_id, 
                          fac_name=fac_name, 
                          address=address, 
                          city=city, 
                          state=state, 
                          zipcode=zipcode, 
                          program_name=program_name)
        db.session.add(program)

    db.session.commit()

def load_recordings():
    ocean = Recording(name='Ocean', 
                      description="""Relaxing Ocean Sounds recording from Tanah 
                      Lot in Bali. Tanah Lot is a rocky area on the south-west 
                      coast of Bali and home to the ancient Hindu pilgrimage 
                      temple Pura Tanah Lot.""", 
                      file_path='/static/audio/Indonesia_Bali_TanahLot_Ocean_Waves_SC.mp3')
    park = Recording(name='Park', 
                     description="""Five minutes at the Echo Park Lake in Los Angeles. 
                     You can hear birds, people, water, and traffic.""", 
                     file_path='/static/audio/USA_Los_Angeles_Echo_Park_Ambiance_People_Stereo.mp3')
    stream = Recording(name='Stream', 
                     description="""A flowing river has a relaxing and healing 
                     sound. Birds sing in the background while water flows.""", 
                     file_path='/static/audio/Bachlauf_Binaural_Biberach.mp3')
    db.session.add_all([ocean, park, stream])

def load_dummy_data_with_real_programs_and_recordings():
        
    print('Real Programs')
    load_programs()

    print('User')
    denise = User(username='denisecodes', password='Python', 
                  first_name='Denise', last_name='Codes', email='denise@codes.com')
    roy = User(username='roycodes', password='Python',
                  first_name='Roy', last_name='Codes', email='roy@codes.com')
    leo = User(username="leocodes", password="Java",
                  first_name='Leo', last_name='Codes', email='leo@codes.com')
    turing = User(username='turingcodes', password='JavaScript',
                  first_name='Turing', last_name='Codes', email='turing@codes.com')

    print('UserProgram')
    program_1 = db.session.query(Program).filter(Program.program_id==1).one()
    program_2 = db.session.query(Program).filter(Program.program_id==1).one()
    program_3 = db.session.query(Program).filter(Program.program_id==1).one()

    denise.programs.append(program_1)
    denise.programs.append(program_2)
    denise.programs.append(program_3)
    roy.programs.append(program_2)
    roy.programs.append(program_3)

    print('Recording')
    load_recordings()

    print('UserRecording')
    ocean = db.session.query(Recording).filter(Recording.recording_id==1).one()
    park = db.session.query(Recording).filter(Recording.recording_id==2).one()
    stream = db.session.query(Recording).filter(Recording.recording_id==3).one()

    denise.recordings.append(ocean)
    denise.recordings.append(park)
    denise.recordings.append(stream)
    roy.recordings.append(park)
    roy.recordings.append(stream)

    db.session.add_all([denise, roy, leo, turing])
    db.session.commit()

    print('Message')
    family = Message(message_type='Family', message='I am not feeling well. I will contact you when I start feeling better.')
    boss = Message(message_type='Co-worker', message='I am out sick today. Please message me if there are any immediate deliverables for today.')
    friend = Message(message_type='Friend', message='I really wanted to see you but I cannot visit with you today. Will get in touch when I am feeling better.')
    denise.messages.append(family)
    denise.messages.append(boss)
    denise.messages.append(friend)
    roy.messages.append(boss)
    roy.messages.append(friend)

    db.session.add_all([family, boss, friend])
    db.session.commit()


if __name__ == '__main__':
    connect_to_db(app)

    # create the tables
    db.create_all()

    # import dummy data
    ###load_dummy_data()
    load_dummy_data_with_real_programs_and_recordings()

