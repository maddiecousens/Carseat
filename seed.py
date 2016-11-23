from model import User, Ride, Rider, Request

from model import connect_db, db
from server import app

from sqlalchemy import func

from datetime import datetime, timedelta

import csv

import geocoder
import pytz
import time

import os
import googlemaps
from collections import defaultdict
from helperfunctions import state_to_timezone, miles_to_degrees


GOOGLE_KEY = os.environ["GOOGLE_KEY"]

def all_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    print "deleting data"
    db.drop_all()
    
    db.create_all()

   # Add sample employees and departments
    maddie = User(user_id=1, fb_userid="10154085900708339", first_name="Maddie", last_name="Cousens", age=24, email="maddie@", password="doge1", image="https://s-media-cache-ak0.pinimg.com/236x/3a/8e/6e/3a8e6eec898c6f3d1c9352503a9c8e37.jpg")
    ahmad = User(user_id=2, fb_userid="108875526264733", first_name="Ahmad", last_name="Alawad", age=30, email="ahmad@", password="maddie2", image="http://theverybesttop10.com/wp-content/uploads/2014/10/Top-10-Images-of-Cats-Driving-2.jpg")
    carl = User(user_id=3, fb_userid="100014238157245", first_name="Aretha", last_name="Franklin", age=51, email="carl@", password="maddie3", image="https://i.ytimg.com/vi/BWAK0J8Uhzk/hqdefault.jpg")
    graham = User(user_id=4, fb_userid="100014205218090", first_name="Graham", last_name="Egan", age=27, email="graham@", password="maddie4", image="http://67.media.tumblr.com/tumblr_md019wlf781rz4vr8o1_1280.jpg")
    grom= User(user_id=5, fb_userid="105608939924154", first_name="Grom", last_name="Gromoth", age=27, email="grom@", password="maddie5", image="https://s-media-cache-ak0.pinimg.com/originals/84/42/a7/8442a778bf0b163a3c30aefe7a64be61.jpg")
    thomoth = User(user_id=6, fb_userid="100014168388615", first_name="Beyonce", last_name="Knowles", age=27, email="thomoth@", password="maddie6", image="https://s-media-cache-ak0.pinimg.com/originals/13/44/06/134406e512f3ab5b252df70df541bf56.jpg")
    lexie = User(user_id=7, fb_userid="100014175948968", first_name="Lexie", last_name="Cousens", age=27, email="lexie@", password="maddie7", image="http://www.zercustoms.com/news/images/Subaru-dog-driving-lessons-b.jpg")
    ryan = User(user_id=8, fb_userid="110433086107763", first_name="Ryan", last_name="Neal", age=27, email="ryan_xskfbpi_neal@tfbnw.net", password="testuser8", image="https://s-media-cache-ak0.pinimg.com/originals/28/c7/ad/28c7adffc9af705dcd8a8b77b1a9c0e8.jpg")

    # rider1 = Rider(id=1, ride_id=1, user_id=3, seats=2)
    # rider2 = Rider(id=2, ride_id=1, user_id=4, seats=2)
    # rider3 = Rider(id=3, ride_id=2, user_id=1, seats=1)
    # rider4 = Rider(id=4, ride_id=2, user_id=4, seats=1)

    # request1 = Request(ride_id=1, requester=2, seats=2)
    # request2 = Request(ride_id=3, requester=3, seats=2)
    # request3 = Request(ride_id=5, requester=3, seats=3)
    # request4 = Request(ride_id=5, requester=1, seats=1)

    db.session.add_all([maddie, ahmad, carl, graham, grom, thomoth, lexie, ryan])
    db.session.commit()

    with open('seed-data/rides_seed.csv', 'rb') as ride_data:

        reader = csv.reader(ride_data, quotechar="'", delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        reader.next()
        gmaps = googlemaps.Client(key=GOOGLE_KEY)

        geocode = defaultdict(defaultdict)

        for row in reader:
            route = row[15]

            if not geocode[route]:

                start_lat = row[3]
                start_lng = row[4]
                end_lat = row[5]
                end_lng = row[6]
                time.sleep(1)
                g_start = geocoder.google('{}, {}'.format(start_lat, start_lng))
                time.sleep(1)
                g_end = geocoder.google('{}, {}'.format(end_lat, end_lng))

                geocode[route]['start_lat'] = start_lat
                geocode[route]['start_lng'] = start_lng
                geocode[route]['start_number'] = g_start.housenumber
                geocode[route]['start_street'] = g_start.street
                geocode[route]['start_city'] = g_start.city
                geocode[route]['start_state'] = g_start.state
                geocode[route]['start_zip'] = g_start.postal

                geocode[route]['end_lat'] = end_lat
                geocode[route]['end_lng'] = end_lng
                geocode[route]['end_number'] = g_end.housenumber
                geocode[route]['end_street'] = g_end.street
                geocode[route]['end_city'] = g_end.city
                geocode[route]['end_state'] = g_end.state
                geocode[route]['end_zip'] = g_end.postal

                start_time = datetime.strptime('4:00 PM', '%I:%M %p')
                today = datetime.now().date()
                start_datetime = datetime.combine(datetime.now().date() + timedelta(days = 1), start_time.time())

                tz = state_to_timezone(geocode[route]['start_state'])
                start_time_aware = pytz.timezone(tz).localize(start_datetime)

                print '\n\n{},{},{},{},{}\n\n'.format(start_time, today, start_datetime, tz, start_time_aware)

                try:
                    directions_result = gmaps.directions("{},{}".format(start_lat, start_lng),
                                                     "{},{}".format(end_lat, end_lng),
                                                     traffic_model='best_guess',
                                                     departure_time=start_time_aware)

                    print 'made it past directions_result'

                    geocode[route]['duration'] = directions_result[0]['legs'][0]['duration']['text']

                    geocode[route]['mileage'] = directions_result[0]['legs'][0]['distance']['text']

                    print '\n\nduration: {}, mileage{}\n\n'.format(geocode[route]['duration'], geocode[route]['mileage'])
                except Exception,e: 
                    print '\n\nDuration/Mileage API Failed\n\n'
                    geocode[route]['mileage'] = None
                    geocode[route]['duration'] = None
                    print "Unexpected error:", start_lat, start_lng, end_lat, end_lng
                    print str(e)


            start_time = datetime.strptime(row[7], '%I:%M %p')
            today = datetime.now().date()
            day_offset = int(row[14])
            start_datetime = datetime.combine(datetime.now().date() + timedelta(days = day_offset), start_time.time())

            tz = state_to_timezone(geocode[route]['start_state'])
            # localize to US/Pacific
            start_time_aware = pytz.timezone(tz).localize(start_datetime)

            # Normalize to UTC
            start_time_utc = pytz.utc.normalize(start_time_aware)

            ride = Ride(driver=row[0],
                        seats=row[1],
                        cost=row[2],

                        # Start Location
                        start_lat=geocode[route]['start_lat'],
                        start_lng=geocode[route]['start_lng'],
                        start_number=geocode[route]['start_number'],
                        start_street=geocode[route]['start_street'],
                        start_city=geocode[route]['start_city'],
                        start_state=geocode[route]['start_state'],
                        start_zip=geocode[route]['start_zip'],
                        # End Location
                        end_lat=geocode[route]['end_lat'],
                        end_lng=geocode[route]['end_lng'],
                        end_number=geocode[route]['end_number'],
                        end_street=geocode[route]['end_street'],
                        end_city=geocode[route]['end_city'],
                        end_state=geocode[route]['end_state'],
                        end_zip=geocode[route]['end_zip'],

                        # Date/Time
                        start_timestamp=start_time_utc,
                        
                        #Details
                        car_type=row[9],
                        luggage=row[10],
                        comments=row[11],
                        pickup_window=row[12],
                        detour=row[13],
                        mileage=geocode[route]['mileage'],
                        duration=geocode[route]['duration']
                        )
    
            db.session.add(ride)
            db.session.commit()
        print geocode
    print "adding data"

def example_data():
    # In case this is run more than once, empty out existing data
    Request.query.delete()
    Rider.query.delete()
    Ride.query.delete()
    User.query.delete()

    maddie = User(user_id=1, fb_userid="10154085900708339", first_name="Maddie", last_name="Cousens", age=24, email="maddie@", password="doge1", image="https://s-media-cache-ak0.pinimg.com/236x/3a/8e/6e/3a8e6eec898c6f3d1c9352503a9c8e37.jpg")
    ahmad = User(user_id=2, fb_userid="108875526264733", first_name="Ahmad", last_name="Alawad", age=30, email="ahmad@", password="maddie2", image="http://theverybesttop10.com/wp-content/uploads/2014/10/Top-10-Images-of-Cats-Driving-2.jpg")
    carl = User(user_id=3, fb_userid="100014238157245", first_name="Aretha", last_name="Franklin", age=51, email="carl@", password="maddie3", image="https://i.ytimg.com/vi/BWAK0J8Uhzk/hqdefault.jpg")
    graham = User(user_id=4, fb_userid="100014205218090", first_name="Graham", last_name="Egan", age=27, email="graham@", password="maddie4", image="http://67.media.tumblr.com/tumblr_md019wlf781rz4vr8o1_1280.jpg")
    grom= User(user_id=5, fb_userid="105608939924154", first_name="Grom", last_name="Gromoth", age=27, email="grom@", password="maddie5", image="https://s-media-cache-ak0.pinimg.com/originals/84/42/a7/8442a778bf0b163a3c30aefe7a64be61.jpg")
    thomoth = User(user_id=6, fb_userid="100014168388615", first_name="Beyonce", last_name="Knowles", age=27, email="thomoth@", password="maddie6", image="https://s-media-cache-ak0.pinimg.com/originals/13/44/06/134406e512f3ab5b252df70df541bf56.jpg")
    lexie = User(user_id=7, fb_userid="100014175948968", first_name="Lexie", last_name="Cousens", age=27, email="lexie@", password="maddie7", image="http://www.zercustoms.com/news/images/Subaru-dog-driving-lessons-b.jpg")
    ryan = User(user_id=8, fb_userid="110433086107763", first_name="Ryan", last_name="Neal", age=27, email="ryan_xskfbpi_neal@tfbnw.net", password="testuser8", image="https://s-media-cache-ak0.pinimg.com/originals/28/c7/ad/28c7adffc9af705dcd8a8b77b1a9c0e8.jpg")

    db.session.add_all([maddie, ahmad, carl, graham, grom, thomoth, lexie, ryan])
    db.session.commit()

    with open('seed-data/rides_seed_testdb.csv', 'rb') as ride_data:

        reader = csv.reader(ride_data, quotechar="'", delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        reader.next()
        gmaps = googlemaps.Client(key=GOOGLE_KEY)

        geocode = defaultdict(defaultdict)

        for row in reader:
            route = row[15]

            if not geocode[route]:

                start_lat = row[3]
                start_lng = row[4]
                end_lat = row[5]
                end_lng = row[6]
                time.sleep(1)
                g_start = geocoder.google('{}, {}'.format(start_lat, start_lng))
                time.sleep(1)
                g_end = geocoder.google('{}, {}'.format(end_lat, end_lng))

                geocode[route]['start_lat'] = start_lat
                geocode[route]['start_lng'] = start_lng
                geocode[route]['start_number'] = g_start.housenumber
                geocode[route]['start_street'] = g_start.street
                geocode[route]['start_city'] = g_start.city
                geocode[route]['start_state'] = g_start.state
                geocode[route]['start_zip'] = g_start.postal

                geocode[route]['end_lat'] = end_lat
                geocode[route]['end_lng'] = end_lng
                geocode[route]['end_number'] = g_end.housenumber
                geocode[route]['end_street'] = g_end.street
                geocode[route]['end_city'] = g_end.city
                geocode[route]['end_state'] = g_end.state
                geocode[route]['end_zip'] = g_end.postal

                start_time = datetime.strptime('4:00 PM', '%I:%M %p')
                today = datetime.now().date()
                start_datetime = datetime.combine(datetime.now().date() + timedelta(days = 1), start_time.time())

                tz = state_to_timezone(geocode[route]['start_state'])
                start_time_aware = pytz.timezone(tz).localize(start_datetime)

                print '\n\n{},{},{},{},{}\n\n'.format(start_time, today, start_datetime, tz, start_time_aware)

                try:
                    directions_result = gmaps.directions("{},{}".format(start_lat, start_lng),
                                                     "{},{}".format(end_lat, end_lng),
                                                     traffic_model='best_guess',
                                                     departure_time=start_time_aware)

                    print 'made it past directions_result'

                    geocode[route]['duration'] = directions_result[0]['legs'][0]['duration']['text']

                    geocode[route]['mileage'] = directions_result[0]['legs'][0]['distance']['text']

                    print '\n\nduration: {}, mileage{}\n\n'.format(geocode[route]['duration'], geocode[route]['mileage'])
                except Exception,e: 
                    print '\n\nDuration/Mileage API Failed\n\n'
                    geocode[route]['mileage'] = None
                    geocode[route]['duration'] = None
                    print "Unexpected error:", start_lat, start_lng, end_lat, end_lng
                    print str(e)


            start_time = datetime.strptime(row[7], '%I:%M %p')
            today = datetime.now().date()
            day_offset = int(row[14])
            start_datetime = datetime.combine(datetime.now().date() + timedelta(days = day_offset), start_time.time())

            tz = state_to_timezone(geocode[route]['start_state'])
            # localize to US/Pacific
            start_time_aware = pytz.timezone(tz).localize(start_datetime)

            # Normalize to UTC
            start_time_utc = pytz.utc.normalize(start_time_aware)

            ride = Ride(driver=row[0],
                        seats=row[1],
                        cost=row[2],

                        # Start Location
                        start_lat=geocode[route]['start_lat'],
                        start_lng=geocode[route]['start_lng'],
                        start_number=geocode[route]['start_number'],
                        start_street=geocode[route]['start_street'],
                        start_city=geocode[route]['start_city'],
                        start_state=geocode[route]['start_state'],
                        start_zip=geocode[route]['start_zip'],
                        # End Location
                        end_lat=geocode[route]['end_lat'],
                        end_lng=geocode[route]['end_lng'],
                        end_number=geocode[route]['end_number'],
                        end_street=geocode[route]['end_street'],
                        end_city=geocode[route]['end_city'],
                        end_state=geocode[route]['end_state'],
                        end_zip=geocode[route]['end_zip'],

                        # Date/Time
                        start_timestamp=start_time_utc,
                        
                        #Details
                        car_type=row[9],
                        luggage=row[10],
                        comments=row[11],
                        pickup_window=row[12],
                        detour=row[13],
                        mileage=geocode[route]['mileage'],
                        duration=geocode[route]['duration']
                        )
    
            db.session.add(ride)
            db.session.commit()
        print geocode
    # Add sample employees and departments
    
    rider1 = Rider(id=1, ride_id=1, user_id=7, seats=2)
    rider2 = Rider(id=2, ride_id=1, user_id=8, seats=2)
    rider3 = Rider(id=3, ride_id=2, user_id=7, seats=1)
    rider4 = Rider(id=4, ride_id=2, user_id=8, seats=1)

    request1 = Request(ride_id=9, requester=5, seats=2)
    request2 = Request(ride_id=9, requester=6, seats=2)
    request3 = Request(ride_id=10, requester=5, seats=3)
    request4 = Request(ride_id=10, requester=6, seats=1)

    db.session.add_all([rider1, rider2, rider3, rider4, request1, request2, request3, request4])
    db.session.commit()
    print "added testdb"

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

    all_data()
    set_val_user_id()
    # set_val_rider_id()
    # set_val_ride_id()