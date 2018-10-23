from model import (User, Facility, Program, Recording, Message)
from model import (ProgramStaging, FacilityProgram, UserFacility, UserRecording, UserMessage)
from model import connect_to_db, db 
from server import app
from zeep import Client, helpers
import os
import sys

def load_dummy_data():
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

    angels = Facility(address='100 A St', city='CityOfAngels', 
                      fac_name='fac_name_1', state='CA', zipcode=10000)
    devils = Facility(address='100 B St', city='CityOfDevils', 
                      fac_name='fac_name_2', state='CA', zipcode=20000)
    wizards = Facility(address='100 C St', city='CityOfWizards', 
                       fac_name='fac_name_3', state='CA', zipcode=30000)
    denise.facilities.append(angels)
    denise.facilities.append(devils)
    denise.facilities.append(wizards)
    roy.facilities.append(devils)
    roy.facilities.append(wizards)

    cake = Program(program_name='Cake')
    pudding = Program(program_name='Pudding')
    bread = Program(program_name='Bread')
    angels.programs.append(cake)
    angels.programs.append(pudding)
    angels.programs.append(bread)
    devils.programs.append(pudding)
    devils.programs.append(bread)

    ocean = Recording(name='Ocean', description='Ocean sounds', file_path='/static/ocean')
    wind = Recording(name='Wind', description='Wind sounds', file_path='/static/wind')
    park = Recording(name='Park', description='Park sounds', file_path='/static/park')
    denise.recordings.append(ocean)
    denise.recordings.append(wind)
    denise.recordings.append(park)
    roy.recordings.append(wind)
    roy.recordings.append(park)

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

def load_programs_from_va_into_file():
    license = os.environ['VA_LICENSE']

    client = Client('https://www.va.gov/webservices/PTSD/ptsd.cfc?wsdl')

    output = client.service.PTSD_Program_Locator_query(license)

    order = output[1]['value']['_value_1']
    status = output[2]['value']['_value_1']
    matches = output[3]['value']['_value_1']

    columns = output[0]['value']['columnList']
    data = output[0]['value']['data']

    file = open('programs.txt', 'w')

    for program_dict in data:
        row_data = program_dict['_value_1']

        fac_id = row_data[0]['_value_1']
        fac_name = row_data[1]['_value_1']
        address = row_data[2]['_value_1']
        city = row_data[3]['_value_1']
        state = row_data[4]['_value_1']
        zipcode = row_data[5]['_value_1']
        program_name = row_data[6]['_value_1']

        file.write(f'{fac_id} |{fac_name}|{address}|{city}|{state}|{zipcode}|{program_name}\n')

    file.close()

def load_facilities_and_programs_from_file_and_remove_duplicates():
  """ Load all rows from programs.txt file, remove duplicates, seed tables in database.


  All rows from programs.txt goes into the programs_staging table. 
  The data from the rows is then broken down into two tables: facilities and programs."""

  file = open('programs.txt', 'r')

  # remove diplicates
  staging_set = set()
  facility_set = set()
  program_set = set()
  facility_program_set = set()

  for line in file:
      fac_id, fac_name, address, city, state, zipcode, program_name = line.split('|')
      staging_tup = (fac_id,
                     fac_name,
                     address,
                     city,
                     state,
                     zipcode[:5],
                     program_name)

      facility_tup = (fac_id,
                      fac_name,
                      address,
                      city,
                      state,
                      zipcode)

      program_tup = (program_name,)

      facility_program_tup = (fac_id, program_name)

      staging_set.add(staging_tup)
      facility_set.add(facility_tup)
      program_set.add(program_tup)
      facility_program_set.add(facility_program_tup)

  file.close() 

  # add items to programs_staging table
  for item in staging_set:
      program_staging = ProgramStaging(fac_id=item[0], 
                                       fac_name=item[1], 
                                       address=item[2], 
                                       city=item[3], 
                                       state=item[4], 
                                       zipcode=item[5], 
                                       program_name=item[6])
      db.session.add(program_staging)
  db.session.commit()

  # add items to facilities table
  for item in facility_set:
      facility = Facility(fac_id=item[0], 
                          fac_name=item[1], 
                          address=item[2], 
                          city=item[3], 
                          state=item[4], 
                          zipcode=item[5])
      db.session.add(facility)
  db.session.commit()

  # add items to programs table
  for item in program_set:
      program = Program(program_name=item[0])
      db.session.add(program)
  db.session.commit()

  # create mapping program_name to program_id
  program_dict = {}
  for program in Program.query.all():
      program_dict[program.program_name] = program.program_id

  # add items to facilities_programs table
  for item in facility_program_set:
      program_id = program_dict[item[1]]
      facility_program = FacilityProgram(fac_id=item[0], program_id=program_id)
      db.session.add(facility_program)
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

def load_dummy_users_with_rest_of_data(needsUpdate):
        
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

    print('Real Facilities and Programs')
    if needsUpdate:
        load_programs_from_va_into_file()
    load_facilities_and_programs_from_file_and_remove_duplicates()

    print('UserFacility')
    user_facility_1 = UserFacility(user_id=1, fac_id=53) # Fresno facility
    user_facility_2 = UserFacility(user_id=1, fac_id=119) # San Diego facility 
    user_facility_3 = UserFacility(user_id=1, fac_id=5195) # Menlo Parl facility
    user_facility_4 = UserFacility(user_id=2, fac_id=53)
    user_facility_5 = UserFacility(user_id=2, fac_id=5195)

    db.session.add_all([user_facility_1, user_facility_2, user_facility_3, 
                        user_facility_4, user_facility_5])
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
    # load_dummy_data()
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        load_dummy_users_with_rest_of_data(True)
    else:
        load_dummy_users_with_rest_of_data(False)

