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
    denisedenise = User(username='denisedenise', password='PythonPython',
                        first_name='Denise', last_name='Denise', email='denise.salazar.1210@gmail.com')

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

    db.session.add_all([denise, roy, leo, turing, denisedenise])
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
                      description="Relaxing Ocean Sounds recording from Tanah Lot in Bali. Tanah Lot is a rocky area on the south-west coast of Bali and home to the ancient Hindu pilgrimage temple Pura Tanah Lot.", 
                      file_path='/static/audio/Indonesia_Bali_TanahLot_Ocean_Waves_SC.mp3')
    park = Recording(name='Park', 
                     description="Five minutes at the Echo Park Lake in Los Angeles. You can hear birds, people, water, and traffic.",
                     file_path='/static/audio/USA_Los_Angeles_Echo_Park_Ambiance_People_Stereo.mp3')
    stream = Recording(name='Stream', 
                     description="A flowing river has a relaxing and healing sound. Birds sing in the background while water flows.", 
                     file_path='/static/audio/Bachlauf_Binaural_Biberach.mp3')
    db.session.add_all([ocean, park, stream])
    db.session.commit()

def load_messages():
    family_1 = Message(message_type='Family 1',
                       message="I am taking some time for myself for my mental health. I will reach out to you when I am feeling better.")
    family_2 = Message(message_type='Family 2', 
                     message="I am not feeling well right now. I will contact you when I start feeling better.")
    friend_1 = Message(message_type='Friend 1',
                       message="I need to take some time for myself for my mental health. Let's reconnect soon.")
    friend_2 = Message(message_type='Friend 2', 
                     message="I cannot see you today because I am not feeling well. I really wanted to see you. I will get in touch when I am feeling better.")
    boss_1 = Message(message_type='Boss 1', 
                     message="I'm taking today and tomorrow off to focus on my mental health. Hopefully I'll be back next weekend refreshed and back to 100%. Thank you for understanding.")
    boss_2 = Message(message_type='Boss 2',
                     message="I’m not feeling well and I’ll have to take the day off, but I’ll be back tomorrow")
    team = Message(message_type='Team', 
                   message="I will be unable to attend work today because of personal illness. Please let me know if I can provide any further information. Thank you for understanding.")
    db.session.add_all([family_1, family_2, friend_1, friend_2, boss_1, boss_2, team])
    db.session.commit()

def load_dummy_users_with_rest_of_data():
        
    print('User')
    denise = User(username='denisecodes', password='Python', 
                  first_name='Denise', last_name='Codes', email='denise@codes.com')
    roy = User(username='roycodes', password='Python',
                  first_name='Roy', last_name='Codes', email='roy@codes.com')
    leo = User(username="leocodes", password="Java",
                  first_name='Leo', last_name='Codes', email='leo@codes.com')
    turing = User(username='turingcodes', password='JavaScript',
                  first_name='Turing', last_name='Codes', email='turing@codes.com')
    denisedenise = User(username='denisedenise', password='PythonPython',
                        first_name='Denise', last_name='Denise', email='denise.salazar.1210@gmail.com')

    db.session.add_all([denise, roy, leo, turing, denisedenise])
    db.session.commit()

    print('Real Programs')
    load_programs()

    print('UserProgram')
    user_program_1 = UserProgram(user_id=1, program_id=1)
    user_program_2 = UserProgram(user_id=1, program_id=2)
    user_program_3 = UserProgram(user_id=1, program_id=3)
    user_program_4 = UserProgram(user_id=2, program_id=2)
    user_program_5 = UserProgram(user_id=2, program_id=3)

    db.session.add_all([user_program_1, user_program_2, user_program_3, 
                        user_program_4, user_program_5])
    db.session.commit()

    print('Recording')
    load_recordings()

    print('UserRecording')
    user_recording_1 = UserRecording(user_id=1, recording_id=1)
    user_recording_2 = UserRecording(user_id=1, recording_id=2)
    user_recording_3 = UserRecording(user_id=1, recording_id=3)
    user_recording_4 = UserRecording(user_id=2, recording_id=2)
    user_recording_5 = UserRecording(user_id=2, recording_id=3)

    db.session.add_all([user_recording_1, user_recording_2, user_recording_3, 
                        user_recording_4, user_recording_5])
    db.session.commit()

    print('Message')
    load_messages()

    print('UserMessage')
    user_message_1 = UserMessage(user_id=1, message_id=1)
    user_message_2 = UserMessage(user_id=1, message_id=2)
    user_message_3 = UserMessage(user_id=1, message_id=3)
    user_message_4 = UserMessage(user_id=2, message_id=2)
    user_message_5 = UserMessage(user_id=2, message_id=3)

    db.session.add_all([user_message_1, user_message_2, user_message_3, 
                        user_message_4, user_message_5])
    db.session.commit()


if __name__ == '__main__':
    connect_to_db(app)

    # create the tables
    db.create_all()

    # import dummy data
    ###load_dummy_data()
    load_dummy_users_with_rest_of_data()

