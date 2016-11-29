[![N|Solid](https://i.imgsafe.org/ce014708f3.png)](http://carseat.maddiecousens.com/)

App by **Maddie Cousens**, read more about the devloper on her [LinkedIn]<br>
Deployed Site: [carseat.maddiecousens.com]<br>

**Carseat** is a green platform for connecting travelers with open seats in cars. Travelers can efficiently search the ride database by location, date, pickup time, and cost. Drivers can post rides, specifying details such as drop-off and pickup-points, seats available, space for luggage, cost, and flexibility on pick-up time and detours. A request system allows drivers to approve travelers for their trip.

## Table of Contents
* [Technologies Used](#techused)
* [Features](#features)
* [Setup Installation](#setup)

## <a name="techused"></a>Technologies Used
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, Scrapy<br>
__Frontend:__ Javascript, jQuery, AJAX, Bootstrap<br>
__APIs:__ Google Maps: Places, Directions, Geocode API, Facebook OAuth<br>
__Deployed:__ Heroku<br>

Dependencies in requirements.txt

## <a name="features"></a>Features
Search for rides by location.<br>
Tech Highlights: Google Maps Places API Autocomplete<br>
![autocomplete](/static/img/_readme/autocomplete.gif)

Sort Rides by Departure Time, Date, Cost<br>
Tech Highlights: All toggles synced to jquery event listener which makes AJAX call and re-renders DOM via Javascript.<br>
![search_toggles](/static/img/_readme/search_toggles.gif)

Add Search Locations, Reverse Input<br>
Tech Highlights: Google Maps Places API - Autocomplete, Javascript<br>
![reverse_input](/static/img/_readme/reverse_input.gif)

Pagination<br>
Tech Highlights: AJAX, Jquery, SQLAlchemy<br>
![pagination](/static/img/_readme/pagination.png)

Request Seats & Facebook OAuth Login<br>
Tech Highlights: Facebook OAuth<br>
![login](/static/img/_readme/login.gif)

View Route<br>
Tech Highlights: Google Maps API<br>
![login](/static/img/_readme/view_route.gif)

Sort by Time, Cost, Date<br>
![login](/static/img/_readme/sort_by.gif)

Approve/Reject Requests<br>
![login](/static/img/_readme/approve_reject.gif)

Post Ride
![login](/static/img/_readme/post_ride.png)

## <a name="setup"></a>Setup and Installation
hi




   [LinkedIn]: https://www.linkedin.com/in/maddiecousens
   [carseat.maddiecousens.com]: http://carseat.maddiecousens.com/
   
