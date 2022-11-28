from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(conn.users.users.find())

@user.post('/users', tags=["users"])
def create_user(user: User):
    newUser = dict(user)
    newUser["password"] = sha256_crypt.encrypt(newUser["password"])
    del newUser["id"]
    id = conn.users.users.insert_one(newUser).inserted_id
    createdUser = conn.users.users.find_one({"_id": id})
    print(createdUser)
    return {
        "message": "Usuario creado exitosamente",
        "content": userEntity(createdUser)
    }

@user.get('/user/{id}')
def find_user(id: str):
    return userEntity(conn.users.users.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    userEntity(conn.users.users.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put('/users/{id}')
def update_user(id: str, user: User):
    conn.users.users.find_one_and_update(
        {"_id": ObjectId(id)}, 
        {"$set": dict(user)}
    )
    return userEntity(conn.users.users.find_one({"_id": ObjectId(id)}))