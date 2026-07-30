from datetime import date
from enum import Enum
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskUpdate, TaskPriority, TaskStatus

app = FastAPI(title="Task Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class Task(BaseModel):
    id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: List[str] = Field(default_factory=list)
    is_overdue: bool = False

# In-memory storage for demo purposes
TASK_STORE: List[Task] = []


def compute_overdue(status: TaskStatus, due_date: Optional[date]) -> bool:
    if due_date is None or status == TaskStatus.DONE:
        return False
    return due_date < date.today()


@app.get("/", response_class=HTMLResponse)
def serve_frontend() -> HTMLResponse:
    return HTMLResponse(static_dir.joinpath("index.html").read_text(encoding="utf-8"))

@app.get("/api/tasks", response_model=List[Task])
def list_tasks(
    overdue: Optional[bool] = Query(None),
    tag: Optional[str] = Query(None, min_length=1),
) -> List[Task]:
    for index, task in enumerate(TASK_STORE):
        current_overdue = compute_overdue(task.status, task.due_date)
        if task.is_overdue != current_overdue:
            TASK_STORE[index] = task.model_copy(
                update={"is_overdue": current_overdue}
            )

    tasks = list(TASK_STORE)
    if overdue is not None:
        tasks = [task for task in tasks if task.is_overdue == overdue]
    if tag is not None:
        normalized_tag = tag.strip().lower()
        tasks = [
            task
            for task in tasks
            if any(value.lower() == normalized_tag for value in task.tags)
        ]
    return tasks

@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate) -> Task:
    task = Task(id=str(uuid4()), **task_data.model_dump())
    task.is_overdue = compute_overdue(task.status, task.due_date)
    TASK_STORE.append(task)
    return task

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    for task in TASK_STORE:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update_data: TaskUpdate) -> Task:
    for index, task in enumerate(TASK_STORE):
        if task.id == task_id:
            if update_data.status is not None:
                validate_status_transition(task.status, update_data.status)
            updated = task.model_copy(update=update_data.model_dump(exclude_unset=True))
            updated.is_overdue = compute_overdue(updated.status, updated.due_date)
            TASK_STORE[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: str) -> None:
    for index, task in enumerate(TASK_STORE):
        if task.id == task_id:
            TASK_STORE.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")
