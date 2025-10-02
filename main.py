from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from db import create_all_tables, SessionDep

app = FastAPI(lifespan=create_all_tables)

@app.get("/check-db")
def check_db(session: SessionDep):
    result = session.exec(select()).first()
    return {"db statuts":result}


# --------- MODELOS ---------
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    is_active: bool = True

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    owner_id: int | None = Field(default=None, foreign_key="user.id")

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = Field(default=False)

# --------- CONFIG DB ---------
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --------- API ---------
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --------- CRUD TASK ---------
@app.on_event("startup")
def on_startup():
    create_all_tables()

# --------- ENDPOINTS DE TASK ---------
@app.post("/tasks/", response_model=Task)
def create_task(task: Task, session: SessionDep):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks/", response_model=list[Task])
def read_tasks(session: SessionDep):
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task, session: SessionDep):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.completed = updated_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}