# simple calendar API

## setup
 * move to the directory where you want to clone the preoject:
   `cd path/to/directory`

 * clone the repo:
   `git clone https://github.com/alexwaweru/calendar.git`

 * go to the repo root:
   `cd calendar`

 * create a virtual environment for the requirements installations
   `python -m venv venv`

 * activate the virtual environment
   `venv\Scripts\activate`
 
 * install the dependencies:
   `pip install -r requrements.txt`

 * Start the server:
  `python python app/main/controller/controllers.py`

 * Visit [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) or whatever IP and port the server is configured to run on


 ## test
 * To run tests:
   `python manage.py test`

 ## Examples

 ### A Few Mutations

 * Add User

![](https://github.com/alexwaweru/calendar/blob/master/resources/img/addUser.PNG)

 * Add UserGroup

 ![](https://github.com/alexwaweru/calendar/blob/master/resources/img/addUserGroup.PNG)

 * Add Event

 Adding event automatically sends email to the attendees

![](https://github.com/alexwaweru/calendar/blob/master/resources/img/addEvent.PNG)

* Add Group Event

 Adding group event automatically sends email to every user who is in that user type/group

![](https://github.com/alexwaweru/calendar/blob/master/resources/img/addGroupEvent.PNG)

* Delete Event

 Deleting event automatically sends email to every user who is in that user type/group

![](https://github.com/alexwaweru/calendar/blob/master/resources/img/deleteEvent.PNG)

* Update User

![](https://github.com/alexwaweru/calendar/blob/master/resources/img/updateUser.PNG)