Creating the Database file
- creating the engine which defines the sql url and other informations
- creating a session by binding the engine to the session and changing the arguments for automatic actions
- creating base object to use with the database 

Creating the Models.py file
- creating the model for the database
- model is a component that defines the structure of the table 
- generally model is refered to classes in python

Creating the auth file to manage the authentication
- we need to create api endpoints in the auth file but if we use app = FastAPI auth file will consider as a seperate app
- so if we run main.py the auth.py will not run
- so we want to create a function called router which is capable of routing or including the endpoint from auth.py into main.py
- create a router in the auth.py and import that router into the main file

