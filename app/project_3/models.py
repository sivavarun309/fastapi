from database import Base
from sqlalchemy import Column, Integer, String, Boolean


# Creating the class for the model 
# model is a structure of table or data

class Todos(Base):
    __tablename__ = 'todos'

    # creating the column
    # index define that this column is used as index and also unique
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)

    


