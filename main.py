from fastapi import FastAPI
from src.utils.db import Base,engine
# from src.tasks.models import Taskmodel
from src.tasks.router import task_routes
from src.user.router import user_router

Base.metadata.create_all(engine)

app = FastAPI(title="this is task management application")
app.include_router(task_routes)
app.include_router(user_router)

