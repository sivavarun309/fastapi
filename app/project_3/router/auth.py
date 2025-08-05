from fastapi import APIRouter


# we need to create api endpoints in the auth file but if we use app = FastAPI auth file will consider as a seperate app
# so if we run main.py the auth.py will not run
# so we want to create a function called router which is capable of routing or including the endpoint from auth.py into main.py
router = APIRouter()


@router.get("/auth/")
async def getUser():
    return {"User": "authenticated"}
