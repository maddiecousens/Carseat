"""Modes and database functions for Rideshare Project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from sqlalchemy_utils import ArrowType
from sqlalchemy import cast, Time, Date, case
import arrow
from helperfunctions import order_by_time

db = SQLAlchemy()

##############################################################################
# Database Models



class User(db.Model):
    """User of the site. Can be driver (as of now)"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fb_userid = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    photo = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.now())
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s, name = %s, email=%s, password=%s>" % (self.user_id, 
                                            self.first_name, self.email, self.password)

class Ride(db.Model):
    """A specific ride"""

    __tablename__ = "rides"

    ride_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    driver = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False) #look into this datatype

    # Start Location
    start_lat = db.Column(db.Float(24), nullable=False)
    start_lng = db.Column(db.Float(24), nullable=False)
    start_name = db.Column(db.String(200), nullable=True)
    start_number = db.Column(db.String(50), nullable=True)
    start_street = db.Column(db.String(100), nullable=True)
    start_city = db.Column(db.String(50), nullable=False)
    start_state = db.Column(db.String(15), nullable=False) #add validation
    start_zip = db.Column(db.String(10), nullable=True)
    # End Location
    end_lat = db.Column(db.Float(24), nullable=False)
    end_lng = db.Column(db.Float(24), nullable=False)
    end_name = db.Column(db.String(200), nullable=True)
    end_number = db.Column(db.String(50), nullable=True)
    end_street = db.Column(db.String(100), nullable=True)
    end_city = db.Column(db.String(50), nullable=False)
    end_state = db.Column(db.String(15), nullable=False) #add validation
    end_zip = db.Column(db.String(10), nullable=True)

    # Date/Time
    start_timestamp = db.Column(db.DateTime, nullable=False)
    # end_timestamp = db.Column(db.DateTime, nullable=False)
   
    
    #Details
    mileage = db.Column(db.String(10), nullable=True)   # would there be a way to validate this? API?
    duration = db.Column(db.String(100), nullable=True)
    luggage = db.Column(db.String(50), nullable=True) #number for now.. drop down js
    comments = db.Column(db.Text, nullable=True) #db.Text field??
    pickup_window = db.Column(db.String(50), nullable=True) 
    detour = db.Column(db.String(50), nullable=True) 
    car_type = db.Column(db.String(100), nullable=True)


    user = db.relationship("User",
                            backref=db.backref("rides_offered"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ride ride_id={}, driver={}, start={}, end={}, date={}>".format(self.ride_id, 
            self.driver, self.start_city, self.end_city, self.start_timestamp)


    @classmethod
    def get_rides(cls, **kwargs):
        """Get rides depending on varying search parameters"""


        q = cls.query.options(db.joinedload('user'))

        if kwargs.get('start_lat'):
            deg = float(kwargs.get('deg'))
            start_lat = float(kwargs.get('start_lat'))
            start_lng = float(kwargs.get('start_lng'))

            q = q.filter(
                        ( (cls.start_lat < str(start_lat + deg)) &
                          (cls.start_lat > str(start_lat - deg))
                        ) &
                        ( (cls.start_lng < str(start_lng + deg)) &
                          (cls.start_lng > str(start_lng - deg))
                        ))

        if kwargs.get('end_lat'):
            deg = float(kwargs.get('deg'))
            end_lat = float(kwargs.get('end_lat'))
            end_lng = float(kwargs.get('end_lng'))
            q = q.filter(
                        ( (cls.end_lat < str(end_lat + deg)) &
                          (cls.end_lat > str(end_lat - deg))
                        ) &
                        ( (cls.end_lng < str(end_lng + deg)) &
                          (cls.end_lng > str(end_lng - deg))
                        ))


        if kwargs.get('date_from'):
            date_from = kwargs.get('date_from')

            q = q.filter((cast(cls.start_timestamp, Date) >= date_from))

        if kwargs.get('date_to'):
            date_to = kwargs.get('date_to')
            
            q = q.filter((cast(cls.start_timestamp, Date) <= date_to))

        # print '\n\nhiii: {}\n\n'.format(kwargs.get('start_time'))
       
            #     q = q.filter(cast(cls.start_timestamp, Time) >= start_time)
            # if kwargs.get('start_time') >= '00:00:00' kwargs.get('start_time') and < "00:08:00":
            #     pass

        # print '\n\n\n*STARTTIME*\n{}, {}\n\n\n'.format(start_time, type(start_time))

            # q = q.filter(cast(cls.start_timestamp, Time) >= start_time)

        if kwargs.get('cost'):
            cost = int(kwargs.get('cost'))
            q = q.filter(cls.cost < cost)

        start_time = kwargs.get('start_time')
        print '\n\nhiii: {}\n\n'.format(kwargs.get('start_time'))
        if start_time >= time(0,0) and start_time < time(8,0):
            q1 = q.filter(cast(cls.start_timestamp, Time) >= start_time)
            q2 = q.filter(cast(cls.start_timestamp, Time) < time(8, 0))
            q = q1.intersect(q2)
        else:
            print 'OTHERWISE'
            q1 = q.filter(cast(cls.start_timestamp, Time) >= start_time)
            q2 = q.filter(cast(cls.start_timestamp, Time) < time(8, 0))
            q = q1.union(q2)

        # q = q.order_by(cls.start_timestamp)

        if kwargs.get('order_by') == 'date':
            q = q.order_by(cls.start_timestamp)

        # _whens = {time(0,0) : 65,
        #             time(0,15) : 66,
        #             time(0,30) : 67,
        #             time(0,45) : 68,
        #             time(1,0) : 69,
        #             time(1,15) : 70,
        #             time(1,30) : 71,
        #             time(1,45) : 72,
        #             time(2,0) : 73,
        #             time(2,15) : 74,
        #             time(2,30) : 75,
        #             time(2,45) : 76,
        #             time(3,0) : 77,
        #             time(3,15) : 78,
        #             time(3,30) : 79,
        #             time(3,45) : 80,
        #             time(4,0) : 81,
        #             time(4,15) : 82,
        #             time(4,30) : 83,
        #             time(4,45) : 84,
        #             time(5,0) : 85,
        #             time(5,15) : 86,
        #             time(5,30) : 87,
        #             time(5,45) : 88,
        #             time(6,0) : 89,
        #             time(6,15) : 90,
        #             time(6,30) : 91,
        #             time(6,45) : 92,
        #             time(7,0) : 93,
        #             time(7,15) : 94,
        #             time(7,30) : 95,
        #             time(7,45) : 96,
        #             time(8,0) : 1,
        #             time(8,15) : 2,
        #             time(8,30) : 3,
        #             time(8,45) : 4,
        #             time(9,0) : 5,
        #             time(9,15) : 6,
        #             time(9,30) : 7,
        #             time(9,45) : 8,
        #             time(10,0) : 9,
        #             time(10,15) : 10,
        #             time(10,30) : 11,
        #             time(10,45) : 12,
        #             time(11,0) : 13,
        #             time(11,15) : 14,
        #             time(11,30) : 15,
        #             time(11,45) : 16,
        #             time(12,0) : 17,
        #             time(12,15) : 18,
        #             time(12,30) : 19,
        #             time(12,45) : 20,
        #             time(13,0) : 21,
        #             time(13,15) : 22,
        #             time(13,30) : 23,
        #             time(13,45) : 24,
        #             time(14,0) : 25,
        #             time(14,15) : 26,
        #             time(14,30) : 27,
        #             time(14,45) : 28,
        #             time(15,0) : 29,
        #             time(15,15) : 30,
        #             time(15,30) : 31,
        #             time(15,45) : 32,
        #             time(16,0) : 33,
        #             time(16,15) : 34,
        #             time(16,30) : 35,
        #             time(16,45) : 36,
        #             time(17,0) : 37,
        #             time(17,15) : 38,
        #             time(17,30) : 39,
        #             time(17,45) : 40,
        #             time(18,0) : 41,
        #             time(18,15) : 42,
        #             time(18,30) : 43,
        #             time(18,45) : 44,
        #             time(19,0) : 45,
        #             time(19,15) : 46,
        #             time(19,30) : 47,
        #             time(19,45) : 48,
        #             time(20,0) : 49,
        #             time(20,15) : 50,
        #             time(20,30) : 51,
        #             time(20,45) : 52,
        #             time(21,0) : 53,
        #             time(21,15) : 54,
        #             time(21,30) : 55,
        #             time(21,45) : 56,
        #             time(22,0) : 57,
        #             time(22,15) : 58,
        #             time(22,30) : 59,
        #             time(22,45) : 60,
        #             time(23,0) : 61,
        #             time(23,15) : 62,
        #             time(23,30) : 63,
        #             time(23,45) : 64}


        if kwargs.get('order_by') == 'time':
            sort_order = case(value=(cast(cls.start_timestamp, Time)), whens=order_by_time)
            q = q.order_by(sort_order)


        if kwargs.get('order_by') == 'cost':
            q = q.order_by(cls.cost)



        if kwargs.get('limit'):
            limit_number = int(kwargs.get('limit'))
            q = q.limit(limit_number)

        if kwargs.get('offset'):
            offset_number = int(kwargs.get('offset'))
            q = q.offset(offset_number)

        if kwargs.get('count'):
            rides = q.count()
        else:
            rides = q.all()
        print '\n\n{}\n\n'.format(rides)

        return rides
        

class Rider(db.Model):
    """Association table. Users taking Rides"""

    __tablename__ = "riders"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("rides_taking"))

    ride = db.relationship("Ride",
                            backref=db.backref("riders"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rider id={}, ride_id={}, user_id={}>".format(self.id, 
            self.ride_id, self.user_id)


class Request(db.Model):
    """Requests for rides"""

    __tablename__ = "requests"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    requester = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)


    ride = db.relationship("Ride",
                            backref=db.backref("requests"))

    user = db.relationship("User",
                            backref=db.backref("requests"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Requests id={}, ride_id={}, requester={}, seats={}>".format(self.id, 
            self.ride_id, self.requester, self.seats)


##############################################################################
# Helper Functions

def connect_db(app, db_uri=None):
    """Connect db to Flask app"""

    # Configure connection to PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///rideshare'

    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_db(app)
    print "Connected to Database"