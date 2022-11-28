def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }

def usersEntity(usuarios) -> dict:
    return [userEntity(user) for user in usuarios]