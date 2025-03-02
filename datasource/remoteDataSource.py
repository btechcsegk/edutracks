from models import user 
from config import config


def addUser(new_user: user.User):
    exists = config.usersCollection.find_one({"username": new_user.username})
    if not exists:
        res = config.usersCollection.insert_one(dict(new_user))
        return res
    return "Erorr"

def loginByRole(uname: str, passwd: str):
    exists = config.usersCollection.find_one({"username": uname})
    if exists:
        password = exists['password']
        if password == passwd:
            return exists
        else:
            return "False"
    else:
        return "False"

