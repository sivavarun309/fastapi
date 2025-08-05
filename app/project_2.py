#######################
# Data Validation, Exception Handling, Status Code, Swagger Configuration, Python Request Objects
########################


from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional
from Book import Book

app = FastAPI()             # Fast api is initialized


class Book:
    def __init__(self, id:int, title:str, author:str, description:str, rating:int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "title one", "author one", "book named title one", 5),
    Book(2, "title two", "author two", "book named title two", 7),
    Book(3, "title three", "author three", "book named title three", 8),
    Book(4, "title four", "author one", "book named title four", 6),
    Book(5, "title five", "author three", "book named title five", 6)
]

# Body() function doesnot perform any validation so it is better to avoid using Body function

@app.post("/books/create_book")
async def createBook(book = Body()):
    BOOKS.append(book)
    print(BOOKS)

# pydantic and data validation

# Pydantic
# used for data modeling, data parsing and has efficient error handling
# used in data validation and how to control the data that are coming to fast api

# Validating the datatype of the incoming data

# Creating the pydantic base class for data validation
class bookRequest(BaseModel):
    id:int
    title:str
    author:str
    description:str
    rating:int 

# this will allow us to validate the type of the incoming data

# adding or implementing above pydantic class into the request
@app.post("/books/create_new_book")
async def createNewBook(book : bookRequest):   # the body book will be set to bookRequest type which validate the data

    newBook = Book(**book.model_dump())     # converting the validated body into "Book" objecct same as other values
    BOOKS.append(newBook)


# Data validation like range for the incoming data

# changing the above pydantic class to validate the values of the data
class bookRequestData(BaseModel):
    id: Optional[int] = None   # setting id as the optional parameter so the user don't have to send it 
    title:str  = Field(min_length=3)        # the title data must atleast have 3 char length
    author:str = Field(min_length=2)        # the author data must atleast have 2 char length
    description:str = Field(min_length=1, max_length=100)   # the description data mustbe between 1 and 100 char length
    rating:int = Field(gt=0, lt=11)   # gt is greater than and lt is less than so the value must be between 0 and 6

# Field function which has many parameter option that can be set to validate the data

# id parameter doesn't need to be get from the user instead we assign the incrental value
def withId(book : Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

# above function get the book object which is user input and alters the id of the object and return the book object
    
# implementing value validation into post request
@app.post("/books/create_new_book_validated")
async def createNewBook(book : bookRequestData):  
    newBook = Book(**book.model_dump())   
    BOOKS.append(withId(newBook))  # withId function will assign the new ID for the book object



# implementing put request

# update the book using id
@app.put("/books/")
async def updateBook(book : bookRequestData):
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            BOOKS[i] = Book(**book.model_dump())
            break

# implementing the delete request

# delete the book entry using id
@app.delete("/books/{bookId}")
async def deleteBook(bookId : int):
    for i in range(len(BOOKS)):
        if bookId == BOOKS[i].id:
            BOOKS.pop(i)
            break



'''

# pydantic swagger configuration

# swagger allows us to get the outline of the schema and the default value that need to send and so on
# to configure those for our need we can make changes in the pydantic class where the BaseModel is inherited

# example
class bookRequested(BaseModel):

    id: Optional[int] = Field(description = "Id is not needed to create a new data", default=None)
    # instead of using None direclty Field function has defualt which can set to None
    # because the Field function has more options like description which will display the message in swagger ui schema section
    # if the parameter is set to optional then the default value is must inside the field function

    title:str  = Field(min_length=3)        # the title data must atleast have 3 char length
    author:str = Field(min_length=2)        # the author data must atleast have 2 char length
    description:str = Field(min_length=1, max_length=100)   # the description data mustbe between 1 and 100 char length
    rating:int = Field(gt=0, lt=11)   # gt is greater than and lt is less than so the value must be between 0 and 6

    # under the example of json_schema_extra of the model cofig we can define the 
    # example of the requested body which we can see in the swagger UI
    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"title of the book",
                "author":"author of the book",
                "description":"words about the book",
                "rating": 5
            }
        }
    }

'''


# Validating the path parameters 

# Field function is used to validate the parameter from the body
# like wise "Path" function is used to validate the path parameter
# importing "from fastapi import Path"

@app.get("/books/get_book/{id}")
async def getBook(id : int = Path(gt=0)):   # Path is used to validate with id have to be greater than 0
    for book in BOOKS:
        if id == book.id:
            return book
        
# Validating the Query parameters 

# "Query" function is used to validate the path parameter
# importing "from fastapi import Query"

@ app.get("/books/by_rating/")
async def getBookByRating(rating : int = Query(gt=0, lt=11)):  # Query parameter must be between 0 and 11
    bookToReturn = list()
    for book in BOOKS:
        if rating == book.rating:
            bookToReturn.append(book)
    
    return bookToReturn


# Status Codes

# It is used to help the client to understand what happend on the server side application
# this are international standards on how a client or server should handle the result of the request
# it allows everyone who send the request to know if their submission was successful or not

# 1xx -> Information response: Request Processign
# 2xx -> success: Request Successfully complete
# 3xx -> Redirection: Further action must be complete
# 4xx -> Client Errors: an error was caused by the client
# 5xx -> Server Errors: An error occured on the server

# 2xx Series

# 200: OK -> Standard Response for a successfull request. commonly used for successfull GET requests when data is being returned
# 201: Created -> The request has been successful, creating a new resource. Used when POST creates an entity
# 204: No Content -> The request has been successful, did not create an entity nor return anything. 
#                    Commonly used with PUT requests

# 4xx Series

# 400: Bad Request -> Cannot process due to client error. Commonly used for invalid request methods
# 401: unauthorized -> Client does not have a valid authentication for target resource
# 404: Not Found -> client requested resources can not be found
# 4022: Unprocessable Entity -> Semantic errors in client requests

# 5xx Series

# 500: Internal Server Error -> Generic Error message, when an unexpected issue on the server happened



########################################
# HTTPException

# used is a method which cancels the function and return the status code to the user or clinet
# usually used to send 400 series exceptions

@app.get("/books/{author}")
async def getBookByAuthor(author :str):
    booksToReturn = list()
    for book in BOOKS:
        if author.casefold() == book.author.casefold(): 
            booksToReturn.append(book)
    if len(booksToReturn) > 0:
        return booksToReturn
    else:
        raise HTTPException(status_code=404, detail=f"There is No Book with author named {author}")


# 200 Series specific satus code
# HTTP codes are used from status class from starlette
# must import "from starlette import status"
# we can use all the status code using starlette

@app.get("/books", status_code=status.HTTP_200_OK)       # status_code parameter is used to send the status code 
async def readAllBooks():      
    return BOOKS 

