from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"


# engine will by default perform operation on the single thread that is each thread will handle independent requests
# this will prevent from sharing same connection for different requests
# but fASTAPI will perform task with multiple threads is normal
# to tell the engine the no need to check the same thread for result because there are multiple thread runing in FastApi
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# creating the local session by binding the engine and block all the automatic funciton so that we are in full control of code
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# Creating the database object which we can use to intracte later
Base = declarative_base()

