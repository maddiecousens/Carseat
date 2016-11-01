"""Modes and database functions for Rideshare Project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Database Models

class User(db.Model):
    """User of the site. Can be driver (as of now)"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s, email=%s, password=%s>" % (self.user_id, 
                                            self.email, self.password)

class Ride(db.Model):
    """A specific ride"""

    __tablename__ = "rides"

    ride_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    driver = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_location = db.Column(db.String(100), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("rides_offered"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ride ride_id={}, driver={}, start={}, end={}, date={}>".format(self.ride_id, 
            self.driver, self.start_location, self.end_location, self.date)


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

# class Request(db.Model):
#     """Pending Requests"""

#     id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
#     ride_id = db.Column(db.Integer, nullable=False, db.ForeignKey('riders.ride_id'))
#     user_id = db.Column(db.Integer, nullable=False, db.ForeignKey('users.user_id'))
#     seats = db.Column(db.Integer, nullable=False)

#  id | ride_id | user_id | seats 
# ----+---------+---------+-------
#   1 |       1 |       3 |     2
#   2 |       1 |       4 |     2
#   3 |       2 |       1 |     1
#   4 |       2 |       4 |     1
# (4 rows)

# rideshare=# select * from users;
#  user_id |  name  |  email  | password 
# ---------+--------+---------+----------
#        1 | Maddie | maddie@ | doge1
#        2 | Ahmad  | ahmad@  | doge2
#        3 | Carl   | carl@   | doge3
#        4 | Lexie  | lexie@  | doge4
# (4 rows)

# rideshare=# select * from rides;
#  ride_id | driver | start_location | end_location |            date            | seats 
# ---------+--------+----------------+--------------+----------------------------+-------
#        1 |      1 | SF             | Tahoe        | 2016-10-31 21:17:37.659467 |     4
#        2 |      2 | SF             | LA           | 2016-10-31 21:17:37.659565 |     4









##############################################################################
# Helper Functions

def connect_db(app):
    """Connect db to Flask app"""

    # Configure connection to PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rideshare'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_db(app)
    print "Connected to Database"