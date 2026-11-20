from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body:TaskSchema, db:Session):
    data = body.model_dump()
    new_task = TaskModel(title=data["title"], 
                         description= data["description"],
                         is_completed = data["is_completed"])
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task(db:Session,):
    tasks = db.query(TaskModel).all()
    return tasks


def get_one_task(task_id : int, db:Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task ID is Incorrect")
    
    
    return one_task
    
def update_task(body: TaskSchema, task_id: int, db: Session):
    task = db.get(TaskModel, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task ID is incorrect")

    data = body.model_dump()
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task
    
def delete_task(task_id:int, db:Session):
    task = db.get(TaskModel, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task ID is incorrect")
    
    db.delete(task)
    db.commit()
    
    return None