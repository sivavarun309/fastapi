# full SQL DataBase, Authentication, Authorization, Hashing Passwords

from fastapi import FastAPI
import models    # models file that we created
from database import engine  # database file that we created

from router import auth, todos, admin

app = FastAPI()


# it will create a everything from the database.py and models.py file
# means it will create "todos.db" and a model with all the columns that are mentioned in models.py
# this line will only run if the db is not exist, if we make any change in models.py the database will not update
# because the below line will not run if the database exists

models.Base.metadata.create_all(bind=engine)


# by including api function from auth and todos into to main app
# we can include all the api function from different operations for the cleaner code

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)