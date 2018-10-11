from model import (User, Program, Recording, Message)
from model import (UserProgram, UserRecording, UserMessage)
from model import connect_to_db, db 
from server import app
from zeep import Client, helpers

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

def load_dummy_data_with_real_programs():
        print('User')
        denise = User(username='denisecodes', password='Python', 
                      first_name='Denise', last_name='Codes', email='denise@codes.com')
        roy = User(username='roycodes', password='Python',
                      first_name='Roy', last_name='Codes', email='roy@codes.com')
        leo = User(username="leocodes", password="Java",
                      first_name='Leo', last_name='Codes', email='leo@codes.com')
        turing = User(username='turingcodes', password='JavaScript',
                      first_name='Turing', last_name='Codes', email='turing@codes.com')
        db.session.add_all([denise, roy, leo, turing])
        db.session.commit()

        print('Real Programs')
        load_programs()

        print('UserProgram')
        user_program_1 = UserProgram(user_id=1, program_id=1)
        user_program_2 = UserProgram(user_id=1, program_id=2)
        user_program_3 = UserProgram(user_id=1, program_id=3)
        user_program_4 = UserProgram(user_id=2, program_id=2)
        user_program_5 = UserProgram(user_id=3, program_id=3)

        db.session.add_all([user_program_1, 
                            user_program_2, 
                            user_program_3, 
                            user_program_4, 
                            user_program_5])
        db.session.commit()

        print('Recording')
        ocean = Recording(name='Ocean', description='Ocean sounds', file_path='/static/ocean')
        wind = Recording(name='Wind', description='Wind sounds', file_path='/static/wind')
        park = Recording(name='Park', description='Park sounds', file_path='/static/park')
        denise.recordings.append(ocean)
        denise.recordings.append(wind)
        denise.recordings.append(park)
        roy.recordings.append(wind)
        roy.recordings.append(park)

        db.session.add_all([ocean, wind, park])
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
    load_dummy_data()

