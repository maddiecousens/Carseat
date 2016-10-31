from model import User, Ride, Rider

from model import connect_db, db
from server import app

from sqlalchemy import func

from datetime import datetime

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    print "deleting data"
    db.drop_all()
    db.create_all()
    # User.query.delete()
    # Ride.query.delete()
    # Rider.query.delete()

   # Add sample employees and departments
    maddie = User(user_id=1 ,name="Maddie", email="maddie@", password="doge1")
    ahmad = User(user_id=2 ,name="Ahmad", email="ahmad@", password="doge2")
    carl = User(user_id=3 ,name="Carl", email="carl@", password="doge3")
    lexie = User(user_id=4 ,name="Lexie", email="lexie@", password="doge4")

    # = User(name="", email="", password="")

    sfth =Ride(ride_id=1 ,driver=1, start_location="SF", end_location="Tahoe",date=datetime.now(), seats=4)
    sfla =Ride(ride_id=2 ,driver=2, start_location="SF", end_location="LA",date=datetime.now(), seats=4)

    # Ride(driver=, start_location="", end_location="",date =)

    rider1 = Rider(id=1, ride_id=1, user_id=3, seats=2)
    rider2 = Rider(id=2, ride_id=1, user_id=4, seats=2)
    rider3 = Rider(id=3, ride_id=2, user_id=1, seats=1)
    rider4 = Rider(id=4, ride_id=2, user_id=4, seats=1)

    db.session.add_all([maddie, ahmad, carl, lexie, sfth, sfla, rider1, rider2, rider3, rider4])
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
    set_val_rider_id()
    set_val_ride_id()