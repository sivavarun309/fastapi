# full SQL DataBase, Authentication, Authorization, Hashing Passwords

from fastapi import APIRouter, Depends, Path, HTTPException
from database import  SessionLocal   # database file that we created

from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos
from .auth import get_current_user

router = APIRouter()

# creating dependecy for the authentication so every api function can authenticate the user before doing operations
user_dependency = Annotated[dict, Depends(get_current_user)]
# here get_current_user will check the token for the authenticity

# creating a function to get the DB connection or session

def getDB():                    # In the api we need to open the connection and close it for every api funcitons 
    db = SessionLocal()         # So creating the funciton with "yield" is will be useful
    try:                        # because it make the function run faster and by using "yield" and than closing the function
        yield db                # will only close the funciton after the DB is yield. because yield will not end the function
    finally:                    # 
        db.close()              #


# creating a object for Annotated session instead of using whole line every time
dbDependency = Annotated[Session, Depends(getDB)]

@router.get("/",status_code = status.HTTP_200_OK)
async def readAll(user: user_dependency, db: dbDependency): 
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    return db.query(Todos).filter(Todos.user_id == user.get("id")).all()



@router.get("/todo/{todoId}", status_code=status.HTTP_200_OK)
async def getTodoById(user: user_dependency, db: dbDependency, todoId: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    todoValue = db.query(Todos).filter(Todos.user_id == user.get("id")).filter(Todos.id == todoId).first()  
    if todoValue is not None:                                       
        return todoValue                                             
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
@router.post("/todos", status_code=status.HTTP_200_OK)
async def createTodoEntry(user: user_dependency, entry: TodoRequest, db : dbDependency):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
    todoModel = Todos(**entry.model_dump(), user_id=user.get("id"))
    db.add(todoModel)
    db.commit() 


# creating the put requests
@router.put("/todos/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodoList(user: user_dependency, entry: TodoRequest, db: dbDependency, todoId: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    todoentry = db.query(Todos).filter(Todos.user_id == user.get("id")).filter(Todos.id == todoId).first()
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
@router.delete("/todos/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteEntry(user: user_dependency, db:dbDependency, todoId: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    todoentry = db.query(Todos).filter(Todos.user_id == user.get("id")).filter(Todos.id == todoId).first() 
    if todoentry is None:
        raise HTTPException(status_code=404, detail=f"Todo entry not found for id {todoId}")
    
    db.query(Todos).filter(Todos.id == todoId).delete()   # will delete the entry if above "if" is not executed 
    db.commit()





