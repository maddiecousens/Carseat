[![N|Solid](https://i.imgsafe.org/ce014708f3.png)](http://carseat.maddiecousens.com/)

##### App by **Maddie Cousens**, read more about the developer on her [LinkedIn]<br><br>
###### Deployed Site: [carseat.maddiecousens.com]<br>

**Carseat** is a green platform for connecting travelers with open seats in cars. Travelers can efficiently search the ride database by location, date, pickup time, and cost. Drivers can post rides, specifying details such as drop-off and pickup-points, seats available, space for luggage, cost, and flexibility on pick-up time and detours. A request system allows drivers to approve travelers for their trip.

## Table of Contents
* [Technologies Used](#techused)
* [Features](#features)
* [Setup Installation](#setup)

## <a name="techused"></a>Technologies Used
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy<br>
__Frontend:__ Javascript, jQuery, AJAX, Bootstrap<br>
__APIs:__ Google - Places, Geolocation, Maps, & Directions, Facebook OAuth<br>
__Deployed:__ Heroku<br>

Dependencies in requirements.txt

## <a name="features"></a>Features
##### Search for rides by location.<br>
*Tech Highlights:* Google Maps Places API Autocomplete<br>
![autocomplete](/static/img/_readme/autocomplete.gif)

##### Sort Rides by Departure Time, Date, Cost<br>
*Tech Highlights:* Toggles bound to jQuery event listener, event handlers make AJAX call then re-render search results in DOM via Javascript<br>
![search_toggles](/static/img/_readme/search_toggles.gif)

##### Add Search Locations, Reverse Input<br>
*Tech Highlights:* Google Maps Places Autocomplete API, Javascript<br>
![reverse_input](/static/img/_readme/reverse_input.gif)

##### Pagination
*Tech Highlights:* jQuery event listeners on pagination buttons, event handler makes AJAX call, SQLAlchemy adds offset parameter. Offset stored as html data attribute so 'previous' and 'next' can calculate current page<br>
![pagination](/static/img/_readme/pagination.png)

##### Request Seats & Facebook OAuth Login
*Tech Highlights:* Facebook OAuth, Javascript SDK<br>
![login](/static/img/_readme/login.gif)

##### View Route
*Tech Highlights:* Google Maps API<br>
![login](/static/img/_readme/view_route.gif)

##### Sort by Time, Cost, Date
*Tech Highlights:* SQLAlchemy order_by filter. Custom ordering for Time to handle ordering in UTC<br>
![login](/static/img/_readme/sort_by.gif)

##### ##### Approve/Reject Requests
![login](/static/img/_readme/approve_reject.gif)

##### Post Ride
![login](/static/img/_readme/post_ride.png)

## <a name="setup"></a>Setup and Installation

To run this app localy:

Clone repository:
```
$ git clone https://github.com/maddiecousens/Carseat.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database 'carseat':
```
$ createdb carseat
```
Run seed.py to seed database
```
$ python seed.py
```
Add your own [Google API Key](https://developers.google.com/maps/documentation/javascript/get-api-key) to a `secrets.sh` file. Your file should look like:
```
export GOOGLE_KEY="[YOUR-KEY]"
export DATABASE_URL=postgres:////carseat
```
Source your secrets.sh file:
```
$ source secrets.sh
```
Run the app from the command line.
```
$ python server.py
```




   [LinkedIn]: https://www.linkedin.com/in/maddiecousens
   [carseat.maddiecousens.com]: http://carseat.maddiecousens.com/
   
