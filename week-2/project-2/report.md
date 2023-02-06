# Weather app
This application aims to show weather conditions for a particular city
it is single page view app.

* Main modules for project are Flask, Jinja2, Bootstrap, Pandas, request

## Code Structure
We decided first to do package structure, but for the application and
the size of the project it became a bit to cumbersome. So we opted out
but some leftovers of that idea can be seen. 

## Code dependencies 
All the dependency used for app should be stated in requirements.txt

## How to run code
cd to directory src and run command python weather_app.py.

## Files in src directory
* templates - directory that contains all html sources needed to render
	single page app
* config.ini contains the apikey as well as the url to make API call to
	weatherapi
* init.py to able to find python package. 
* weather app.py runs the application.
* weather api.py runs data cleaning processes

## Weather app.py
Has two function called:
* get error message -> will custom message dependent on user behavior
* index -> main driver of the single page app. 

The index function renders the html via flask decorator app.route
and basically deals with both POST and GET methods. 

Basically the GET method call the standard view of the single page app.
* You will see a city icon plus search field and submit button

The POST method of the index function basically handles the following:
* Missing apiKey, user should be prompted that no API key has been
   passed. The message will then prompted to single page via the results
   variable.

* This will check if city entered by user exists an like "öl" will is
   not city and the api will not find a response and therefore prompt
   pass the nested if statement with results.status.code == 200. And the
   else clausal will be triggered and error message from
   get error message. 

* If response from api call is positive then this handled by some code
   in weather api.py with the function called data parser

## Weather api.py
The solve purpose of the is module is to parse data from the api call
response. 

Since the data is nested and not really easy to retrieve and work with 
they are two main function that needs to mentioned 
* get weather data that parse data and un-nests json-object
* weather stats that basically slice the data into important the ones
	deemed important.

Lastly the data parser is recipe function that calls both function in
series.

Overall comment of the code and what it does.
