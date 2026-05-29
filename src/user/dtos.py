from pydantic import BaseModel

class userschema(BaseModel):
    name : str
    username : str
    password : str
    email : str


class userresponceschema(BaseModel):
    name : str
    username : str
    email : str

class loginschema(BaseModel):
    username : str
    password : str
