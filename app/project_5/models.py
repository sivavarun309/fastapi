from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# Creating the class for the model 
# model is a structure of table or data



# model for users
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    hashed_password = Column(String(255))
    role = Column(String(20))
    active = Column(Boolean, default=True)
    phone_number = Column(String)


class Todos(Base):
    __tablename__ = 'todos'

    # creating the column
    # index define that this column is used as index and also unique
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(50))
    description = Column(String(255))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(Users.id))




    


