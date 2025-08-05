from fastapi import APIRouter, Depends, Path, HTTPException
from database import  SessionLocal   # database file that we created

from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from models import Todos, Users
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

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

# creating get request to get all the todos of all the user
@router.get("/todos", status_code=status.HTTP_200_OK)
async def getUser(user: user_dependency, db: dbDependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail= "Authentication Failed")
    
    todosList = db.query(Todos).all()
    return todosList


# creating the request to view the user details
@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user_details(db: dbDependency, user: user_dependency):
    if user is None and user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authenticaiton Failed")
    
    select_columns = select(Users.email, Users.username,Users.first_name,
                          Users.last_name, Users.role, Users.id,
                            Users.active)
    user_data = db.execute(select_columns).mappings().all()  # db.query() is older and slower so better use select with excecute




    return user_data
#{
#        "email": user_data.email,
#        "user_name": user_data.username,
#        "first_name": user_data.first_name,
#        "last_name": user_data.last_name,
#        "role": user_data.role,
#        "user_id": user_data.id,
#        "active": user_data.active
#        }



