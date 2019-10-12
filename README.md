# Simple Calendar API

## Setup
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
  `python python app/main/controller/graphql_server.py`

 * Visit [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) or whatever IP and port the server is configured to run on


 ## Tests

 * To run tests:
   `python manage.py test`
