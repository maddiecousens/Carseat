from model import User, Ride, Rider, Request

from model import connect_db, db
from server import app

from sqlalchemy import func

from datetime import datetime

import csv

import geocoder
import pytz

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    print "deleting data"
    # db.drop_all()
    db.drop_all()
    db.create_all()
    # User.query.delete()
    # Ride.query.delete()
    # Rider.query.delete()

   # Add sample employees and departments
    maddie = User(user_id=1 ,first_name="Maddie", last_name="Cousens", age=24, email="maddie@", password="doge1", image="https://65.media.tumblr.com/avatar_66b336c742ea_128.png")
    ahmad = User(user_id=2 ,first_name="Ahmad", last_name="Alawad", age=30, email="ahmad@", password="doge2")
    carl = User(user_id=3 ,first_name="Carl", last_name="Tinker", age=51, email="carl@", password="doge3")

    # = User(name="", email="", password="")

    # sfth1 =Ride(ride_id=1 ,driver=1, start_location="SF", end_location="Tahoe",date=datetime.now(), seats=4)
    # sfth2 =Ride(ride_id=2 ,driver=1, start_location="SF", end_location="Tahoe",date=datetime.now(), seats=4)
    # sfla1 =Ride(ride_id=3 ,driver=2, start_location="SF", end_location="LA",date=datetime.now(), seats=5)
    # sfla2 =Ride(ride_id=4 ,driver=2, start_location="SF", end_location="LA",date=datetime.now(), seats=5)


    # Ride(driver=, start_location="", end_location="",date =)

    # rider1 = Rider(id=1, ride_id=1, user_id=3, seats=2)
    # rider2 = Rider(id=2, ride_id=1, user_id=4, seats=2)
    # rider3 = Rider(id=3, ride_id=2, user_id=1, seats=1)
    # rider4 = Rider(id=4, ride_id=2, user_id=4, seats=1)

    request1 = Request(ride_id=1, requester=2, seats=2)
    request2 = Request(ride_id=3, requester=3, seats=2)
    request3 = Request(ride_id=5, requester=3, seats=3)
    request4 = Request(ride_id=5, requester=1, seats=1)

    # db.session.add_all([maddie, ahmad, carl, sfth1, sfth2, sfla1, sfla2, request1, request2, request3, request4])
    db.session.add_all([request1, request2, request3, request4])
    db.session.add_all([maddie, ahmad, carl])

    with open('seed-data/rides_seed.csv', 'rb') as ride_data:
        reader = csv.reader(ride_data, quotechar="'", delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        reader.next()
        for row in reader:
            start_lat = row[3]
            start_lng = row[4]
            end_lat = row[5]
            end_lng = row[6]
            g_start = geocoder.google('{}, {}'.format(start_lat, start_lng))
            print '\n\n'
            print g_start.city, ' --- ', g_start
            print '\n\n'
            g_end = geocoder.google('{}, {}'.format(end_lat, end_lng))
            print '\n\n'
            print g_end.city, ' --- ', g_start
            print '\n\n'

            start_time = datetime.strptime(row[7],'%m/%d/%Y %H:%M:%S')
            start_aware = start_time.replace(tzinfo=pytz.timezone('US/Pacific'))
            end_time = datetime.strptime(row[8],'%m/%d/%Y %H:%M:%S')
            end_aware = end_time.replace(tzinfo=pytz.timezone('US/Pacific'))
            start_utc = start_aware.astimezone(pytz.utc)
            end_utc = end_aware.astimezone(pytz.utc)

            ride = Ride(driver = row[0],
                        seats = row[1],
                        cost = row[2],

                        # Start Location
                        start_lat = start_lat,
                        start_lng = start_lng,
                        start_number = g_start.housenumber,
                        start_street = g_start.street,
                        start_city = g_start.city,
                        start_state = g_start.state,
                        start_zip = g_start.postal,

                        # End Location
                        end_lat = end_lat,
                        end_lng = end_lng,
                        end_number = g_end.housenumber,
                        end_street = g_end.street,
                        end_city = g_end.city,
                        end_state = g_end.state,
                        end_zip = g_end.postal,

                        # Date/Time
                        start_timestamp=start_utc,
                        end_timestamp=end_utc,
                        
                        #Details
                        # pickup_window = datetime.strptime(row[24],'%M'),
                        car_type = row[9],
                        luggage =  row[10],
                        comments = row[11]
                        )
    
            db.session.add(ride)
    db.session.commit()
    print "adding data"

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

def set_val_ride_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Ride.ride_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('rides_ride_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

def set_val_rider_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Rider.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('riders_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

if __name__ == "__main__":
    connect_db(app)

    example_data()
    set_val_user_id()
    # set_val_rider_id()
    # set_val_ride_id()