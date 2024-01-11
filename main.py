from fastapi import FastAPI, HTTPException, Depends
from peewee import PostgresqlDatabase
from models import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Dependency to get the database connection
async def get_db():
    db.connect()
    yield db
    db.close()

origins = [
    "http://localhost",
    "http://localhost:3000", 
     "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/items/")
async def create_item(task: str, db: PostgresqlDatabase = Depends(get_db)):
    try:
        print('jelloadckjahvjn',task)
        task_instance=TodoList(task=task)
        task_copy_instance=TodoListCopy(task=task)
        task_instance.save()
        task_copy_instance.save()
        return {"message": "Item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/display_items/")
async def read_items(db: PostgresqlDatabase = Depends(get_db)):
    items = TodoList.select().dicts()
    items_copy=TodoListCopy.select().dicts()
    return {"items1": list(items), "items2": list(items_copy)}

# Move task between lists
@app.put("/tasks/move/")
async def move_task(task_id: int, new_list: str, db: PostgresqlDatabase = Depends(get_db)):
    try:
        if new_list == "list2":
            task = TodoList.get_by_id(task_id)
            TodoListCopy.create(task=task.task)
            task.delete_instance()
        elif new_list == "list1":
            task = TodoListCopy.get_by_id(task_id)
            TodoList.create(task=task.task)
            task.delete_instance()
        else:
            raise HTTPException(status_code=400, detail="Invalid destination list")
        # db.close()
        return {"message": "Task moved successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/delete/")
async def delete_task(task_id:int, list_name: str, db: PostgresqlDatabase = Depends(get_db)):
    try:
        if list_name == "list1":
            task = TodoList.get_by_id(task_id)
            task.delete_instance()
        elif list_name == "list2":
            task = TodoListCopy.get_by_id(task_id)
            task.delete_instance()
        else:
            raise HTTPException(status_code=400, detail="Invalid list name")

        return {"message": "Task deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
    


