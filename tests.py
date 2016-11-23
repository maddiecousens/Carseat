import unittest
from model import *
from server import app
import server
from seed import *
from helperfunctions import state_to_timezone, miles_to_degrees
from datetime import datetime

class CarseatUnitTestCase(unittest.TestCase):
    """Unit Tests"""

    # helperfunctions.state_to_timezone
    def test_state_to_timezone(self):
        self.assertEqual(state_to_timezone('NY'), 'US/Eastern')

    def test_state_to_timezone2(self):
        self.assertEqual(state_to_timezone(''), 'US/Pacific')

    # helperfunctions.miles_to_degrees
    def test_miles_to_degrees(self):
        self.assertEqual(round(miles_to_degrees(5),5),0.07246)

    # Server functions

    # to_time_string
    def test_to_time_string(self):
        self.assertIn('Tomorrow', server.to_time_string('CA', datetime.now() + timedelta(days = 1)))

    def test_to_time_string2(self):
        self.assertIn('Today', server.to_time_string('CA', datetime.now()))

    # to_utc
    def test_to_utc(self):
        self.assertEqual(str(server.to_utc('CA', datetime.now()).tzinfo), 'UTC')

    def test_to_utc2(self):
        utc_ca = server.to_utc('CA', datetime.now())
        utc_ny = server.to_utc('NY', datetime.now())
        self.assertEqual(utc_ca.utctimetuple().tm_hour - utc_ny.utctimetuple().tm_hour, 3)

    # to_local
    def test_to_local(self):
        self.assertEqual(str(server.to_local('NY', datetime.utcnow()).tzinfo), 'US/Eastern')

    def test_to_local2(self):
        local_ca = server.to_local('CA', datetime.utcnow())
        local_ny = server.to_local('NY', datetime.utcnow())
        self.assertEqual(local_ny.timetuple().tm_hour - local_ca.timetuple().tm_hour, 3)


class FlaskTests(unittest.TestCase):
    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_db(app, "postgresql:///testdb")

        # example_data()
        
    def tearDown(self):
            """Do at end of every test."""

            db.session.close()
            # db.drop_all()

    def test_does_ride_exist(self):
        """Can we find an employee in the sample data?"""

        driver1 = Ride.query.filter(Ride.driver == 1).first()
        self.assertEqual(driver1.user.first_name, "Maddie")

    def test_index(self):
        result = self.client.get('/')
        self.assertIn('<form action="/search" id="indexsearch">', result.data)

    def test_search(self):
        result = self.client.get('/search?query=all')
        self.assertIn('<span>386 mi, Est Travel Time: 5 hours 48 mins</span>', result.data)
        import pdb; pdb.set_trace()

    def test_search2(self):
        result = self.client.get('/search?query=all')
        self.assertIn('<li class="page-number" data-pagenumber="3" id="page-number3"><a href="#">3</a></li>', result.data)

    def test_search3(self):
        result = self.client.get('/search?start-address=Seattle%2C+WA%2C+United+States&searchstring=Seattle%2C+WA%2C+United+States&locality=Seattle&administrative_area_level_1=WA&postal_code=&lat=47.6062095&lng=-122.3320708&end-address=Portland%2C+OR%2C+United+States&searchstring2=Portland%2C+OR%2C+United+States&locality2=Portland&administrative_area_level_1_2=OR&postal_code2=&lat2=45.52306220000001&lng2=-122.67648159999999')
        self.assertIn("""<h5>Seattle, WA 
                    <span class="glyphicon glyphicon-arrow-right"></span>
                       Portland, OR</h5>""", result.data)


    # def test_emps_by_state(self):
    #     """Find employees in a state."""

    #     result = self.client.post("/emps-by-state", data={'state':'California'})

    #     self.assertIn("Nadine", result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()