from model import User, Ride, Rider, Request

from model import connect_db, db
from server import app

from sqlalchemy import func

from datetime import datetime

import csv

# import pytz

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
    maddie = User(user_id=1 ,name="Maddie", email="maddie@", password="doge1")
    ahmad = User(user_id=2 ,name="Ahmad", email="ahmad@", password="doge2")
    carl = User(user_id=3 ,name="Carl", email="carl@", password="doge3")

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

    # request1 = Request(ride_id=1, requester=2, seats=2)
    # request2 = Request(ride_id=1, requester=3, seats=2)
    # request3 = Request(ride_id=3, requester=3, seats=3)
    # request4 = Request(ride_id=3, requester=1, seats=1)

    # db.session.add_all([maddie, ahmad, carl, sfth1, sfth2, sfla1, sfla2, request1, request2, request3, request4])
    # db.session.add_all([maddie, ahmad, carl, request1, request2, request3, request4])
    db.session.add_all([maddie, ahmad, carl])

    with open('seed-data/rides_seed.csv', 'rb') as ride_data:
        reader = csv.reader(ride_data, quotechar="'", delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        reader.next()
        for row in reader:
            ride = Ride(driver = row[0],
                        seats = row[1],
                        cost = row[2],

                        # Start Location
                        start_lat = row[3],
                        start_long = row[4],
                        start_name = row[5],
                        start_number = row[6],
                        start_street = row[7],
                        start_city = row[8],
                        start_state = row[9],
                        start_zip = row[10],

                        # End Location
                        end_lat = row[11],
                        end_long = row[12],
                        end_name = row[13],
                        end_number = row[14],
                        end_street = row[15],
                        end_city = row[16],
                        end_state = row[17],
                        end_zip = row[18],

                        # Date/Time
                        start_timestamp = datetime.strptime(row[19],'%m/%d/%y %H:%M'),
                        end_timestamp = datetime.strptime(row[20],'%m/%d/%y %H:%M'),
                        
                        #Details
                        mileage = row[21],
                        # pickup_window = datetime.strptime(row[24],'%M'),
                        car_type = row[22],
                        luggage =  row[23],
                        comments = row[24]
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