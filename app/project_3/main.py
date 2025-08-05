# full SQL DataBase, Authentication, Authorization, Hashing Passwords

from fastapi import FastAPI, Depends, Path, HTTPException
import models    # models file that we created
from database import engine, SessionLocal   # database file that we created

from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos

from router import auth

app = FastAPI()


# it will create a everything from the database.py and models.py file
# means it will create "todos.db" and a model with all the columns that are mentioned in models.py
# this line will only run if the db is not exist, if we make any change in models.py the database will not update
# because the below line will not run if the database exists

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)  # including the router function for the auth.py to include the auth endpoint 

# creating a function to get the DB connection or session

def getDB():                    # In the api we need to open the connection and close it for every api funcitons 
    db = SessionLocal()         # So creating the funciton with "yield" is will be useful
    try:                        # because it make the function run faster and by using "yield" and than closing the function
        yield db                # will only close the funciton after the DB is yield. because yield will not end the function
    finally:                    # 
        db.close()              #



@app.get("/")
async def readAll(db: Annotated[Session, Depends(getDB)], status_code = status.HTTP_200_OK): 
    return db.query(Todos).all()

# Annotated- imported from Typing, if adds metadata to the argument "db". tells that "db" is a Session object with
#            dependencies of "getDB"
# Session  - imported from sqlalchemy.orm and it is a Session class. which is used to intract with the Database 
#            using methods like query(), add(), commit()
# Depands  - imported from fastapi, in fastapi "Depands" is used to add the dependency to the arguments
#            Dependeny is like a requirements that will be needed by some object to work, like authorization, configurations
#            it is A way to delcare things that are required for the application/function to work by injecting the dependencies
#            Here "db" is a "Session" object that requires or depends on "SessionLocal" which has details about the sql connection
# By using the Annotated to add the metadata info to the argument
# the fastapi will run the dependency to create a Session object automatically whenever the db is called

# creating a object for Annotated session instead of using whole line every time
dbDependency = Annotated[Session, Depends(getDB)]

@app.get("/todo/{todoId}", status_code=status.HTTP_200_OK)
async def getTodoById(db: dbDependency, todoId: int = Path(gt=0)):

    todoValue = db.query(Todos).filter(Todos.id == todoId).first()   # mentioning first will reduce the time because, 
    if todoValue is not None:                                        # we know that there will be only one id that is a match
        return todoValue                                             # because ID here is a primary key
    raise HTTPException(status_code=404, detail="Id not found")


# post requests

# creating the pydantic model for authentication
class TodoRequest(BaseModel):
    
    title: str = Field(min_length=5)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool

    model_config = {
        "json_schema_extra":{
        "example":{
            "title":"Your title",
            "description":"about the task",
            "priority":5,
            "completed":False
        }
    }
    }

# Creating the post request method
@app.post("/todos", status_code=status.HTTP_200_OK)
async def createTodoEntry(entry: TodoRequest, db : dbDependency):
    
    todoModel = Todos(**entry.model_dump())
    db.add(todoModel)
    db.commit() 


# creating the put requests
@app.put("/todos/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodoList(entry: TodoRequest, db: dbDependency, todoId: int = Path(gt=0)):

    todoentry = db.query(Todos).filter(Todos.id == todoId).first()
    if todoentry is None:
        raise HTTPException(status_code=404, detail=f"Todo entry not found for id {todoId}")
    
    todoentry.title = entry.title               # here "todoentry" is a entry fetched from the database
    todoentry.description = entry.description   # we have to change the content of the fetched entry with the entry-
    todoentry.priority = entry.priority         # received from the client or user
    todoentry.completed = entry.completed       # this will tell the sqlalchemy to update the entry because it is fetched
                                                # if we create new model it will lead to create a new entry either with-
    db.add(todoentry)                           # new id or throw error for duplicate id
    db.commit()

# creating the delete request
@app.delete("/todos/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteEntry(db:dbDependency, todoId: int = Path(gt=0)):

    todoentry = db.query(Todos).filter(Todos.id == todoId).first() # this query is used to check the "if" condition below
    if todoentry is None:
        raise HTTPException(status_code=404, detail=f"Todo entry not found for id {todoId}")
    
    db.query(Todos).filter(Todos.id == todoId).delete()   # will delete the entry if above "if" is not executed 
    db.commit()





