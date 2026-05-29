from fastapi import APIRouter,Depends,Path,status
from src.tasks import controller
from src.tasks.dtos import Taskschema,taskschema_update,taskresponceschema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.user.models import Usermodel

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create",response_model=taskresponceschema,status_code=status.HTTP_201_CREATED)
def create_task(body : Taskschema,db:Session = Depends(get_db), user : Usermodel = Depends(is_authenticated)):
    return controller.create_task(body,db,user)

@task_routes.get("/given",response_model=List[taskresponceschema],status_code=status.HTTP_200_OK)
def get_tasks(db:Session = Depends(get_db),user : Usermodel = Depends(is_authenticated)):
    return controller.get_tasks(db,user)

@task_routes.get("/one_task/{task_id}",response_model=taskresponceschema,status_code=status.HTTP_200_OK)
def get_one_task(task_id : int = Path(...,description="given task id",example="1"),db:Session = Depends(get_db),user : Usermodel = Depends(is_authenticated)):
    return controller.get_one_task(task_id,db,user)

@task_routes.put("/update/{task_id}",response_model=taskresponceschema,status_code=status.HTTP_201_CREATED)
def update_task(body : taskschema_update,task_id : int = Path(...,description="given task id",example="1"),db:Session = Depends(get_db),user : Usermodel = Depends(is_authenticated)):
    return controller.update_task(body,task_id,db,user)

@task_routes.delete("/delete/{task_id}",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id : int ,db:Session = Depends(get_db),user : Usermodel = Depends(is_authenticated)):
    return controller.delete_task(task_id,db,user)