from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv


from routes.auth import auth_router
from routes.todo import todo_router
from routes.user import user_router


load_dotenv()

app = FastAPI()



origins = ["http://127.0.0.1:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(user_router)
