from src.tasks.dtos import Taskschema,taskschema_update
from sqlalchemy.orm import Session
from src.tasks.models import Taskmodel
from fastapi import HTTPException
from src.user.models import Usermodel   

def create_task(body : Taskschema,db : Session,user:Usermodel):
    data = body.model_dump()
    new_task = Taskmodel(title = data['title'],description = data['description'],
    is_completed = data["is_completed"],
    user_id = user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db: Session,user:Usermodel):
    tasks = db.query(Taskmodel).filter(Taskmodel.user_id == user.id)
    return tasks



def get_one_task(task_id : int,db: Session):
    one_task = db.query(Taskmodel).get(task_id)
    if not one_task:
        return HTTPException(status_code=404,detail="task id is incorrect")
    
    return one_task


def update_task(body : taskschema_update,task_id : int ,db : Session,user : Usermodel):
    one_task = db.query(Taskmodel).get(task_id)
    if not one_task:
        return HTTPException(status_code=404,detail="task id is incorrect")
    
    if one_task.user_id != user.id:
        return HTTPException(404,details = "you are not allowed for this task")

    body = body.model_dump(exclude_unset=True)
    for field,value in body.items():
        setattr(one_task,field,value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task

def delete_task(task_id : int ,db : Session,user : Usermodel):
    one_task = db.query(Taskmodel).get(task_id)
    if not one_task:
        return HTTPException(status_code=404,detail="task id is incorrect")

    if one_task.user_id != user.id:
        return HTTPException(404,details = "you are not allowed for this task")


    db.delete(one_task)
    db.commit()

    return None 