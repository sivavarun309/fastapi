from fastapi import FastAPI, Body

app = FastAPI()             # Fast api is initialized



BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")       # define the endpoint url for the function below
async def readAllBooks():      # fastapi will work fine even without async but ascync is used to reduce the waitig time
    return BOOKS   


# Dynamic parameter in path parameter
# while defining the path we can define the dynamic parameter inside the paranthesis 
# the word inside the paranthesis will act as a variable which can be used inside the respective function

# unlike in general python the funcitons here is called using the endpoint
# rather than the function name so providing the same name for function is possible

@app.get("/books/{dynamicParam}")
async def readAllBooks(dynamicParam : str):    # here ":str" means that this function will only accept string
                                               # and all the paramter provided inside the path parameter is converted to string
    for book in BOOKS:
        if dynamicParam.casefold() == book.get("title").casefold():
            return book


# In path parameter the ordering of the api function is important 

# Here the below function will not be called if the "/books/myBook" endpoint is called
# instead the above function  "/books/{dynamicParam}" will be called
# here "/myBook" is considered as a dynamic parameter because python will always checks by top to bottom order
# and "/books/{dynamicParam}" satisfies the the endpoint  "/books/myBook" the above function is called

# to make it work "@app.get("/books/myBook")" must be provide above the "@app.get("/books/{dynamicParam}")"
@app.get("/books/myBook")
async def readAllBooks(dynamicParam : str):    
    return {'Favorite Book': "MyBook"}


# Query Parameters

# the parameters that has been attached after the "?" in the request
# its a name= value pairs

# instead of getting the parameter through the path of the endpoint 
# in query parameter it is passed directly into the api function with the defined parameter name or key

# here providing "/books/" will differ the endpoint from "/books"
# so it won't interfere with the "/books" endpoint

# if "/books" is mentioned in the query parameter below, it won't work because "/books" is taken from 
# the api function of the above path parameter api fuction

@app.get("/books/")      # make sure to provide the "/" at the end for the query paramters
async def readBookByCategory(category : str):
    booksToReturn = []
    for book in BOOKS:
        if category.casefold() == book.get('category').casefold():
            booksToReturn.append(book)
        
    return booksToReturn


# path parameter in combined with query parameter

# Here both the pathparameter and query parameter is used
# {} for path parameter and "/" at the end for query parameter and query parameter is received via api function

@app.get("/books/{author}/")
async def readByAuthorAndCategory( author:str, category:str):   # parameter doesn't matter
    bookToReturn = []
    for book in BOOKS:
        if author.casefold() == book.get("author").casefold() and category.casefold() == book.get("category").casefold():
            bookToReturn.append(book)

    return bookToReturn 


# post request

# used to create a data 
# it can have a body where the user can send the entire new data to be added

@app.post("/books/create_book")
async def createBook(newBook = Body()):   # here Body() is used to get the data from the body of the request mus be imported
    BOOKS.append(newBook)                 # if the recived format matched with exixting format it can be directly appended

# here Body() is used to get the raw data of the body
# there are other objects or class like Request, Form, File, and we can use pydantic Basemodel to structure the body 

# put request

# used to update the data
# it has the body same as post resquest but instead of adding the new entry in put we update a exicting data or entry

@app.put("/books/update_book")
async def updateBooks(book = Body()):
    for i in range(len(BOOKS)):
        if book.get("title").casefold() == BOOKS[i].get("title").casefold():
            BOOKS[i] = book
    
    return {"Result":"Success"}



# Delete request

# used to delete the data or entry
# the key to delete the value is given through the path parameter

@app.delete("/books/delete_book/{bookTitle}")
async def deleteBook(bookTitle : str):
    for i in range(len(BOOKS)):
        if bookTitle.casefold() == BOOKS[i].get("title").casefold():
            BOOKS.pop(i)
            break
    return {"Result":"Success"}






