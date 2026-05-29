from pydantic import BaseModel,Field
from typing import Annotated

class Taskschema(BaseModel):
    title : str
    description : str
    is_completed : bool = False

class taskschema_update(BaseModel):
    title : Annotated[str,Field(default=None)]
    description : Annotated[str,Field(default=None)]
    is_completed : Annotated[bool,Field(default=None)]

class taskresponceschema(BaseModel):
    id : int 
    title : str 
    description : str 
    is_completed : bool 