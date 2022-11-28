from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title= "API REST CON FASTAPI Y MONGODB",
    description= "Siemple api rest para practicar"
)

app.include_router(user)