from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, validator


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


def normalize_tags(value):
    if value is None:
        return []
    if isinstance(value, str):
        value = [tag.strip() for tag in value.split(",")]
    if not isinstance(value, list):
        raise TypeError("tags must be a list")

    normalized = []
    for tag in value:
        if tag is None:
            continue
        tag_text = str(tag).strip()
        if not tag_text:
            continue
        if len(tag_text) > 20:
            raise ValueError("each tag must be 20 characters or fewer")
        normalized.append(tag_text)

    if len(normalized) > 5:
        raise ValueError("at most 5 tags are allowed")
    return normalized


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

    @validator("title")
    def title_not_blank(cls, v: str) -> str:
        if v is None or not v.strip():
            raise ValueError("title must not be empty or whitespace")
        return v

    @validator("tags", pre=True)
    def clean_tags(cls, v):
        return normalize_tags(v)

    class Config:
        extra = "forbid"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @validator("title")
    def title_strip_and_validate(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("title must not be empty or whitespace")
        if len(v) > 200:
            raise ValueError("title too long")
        return v

    @validator("tags", pre=True)
    def clean_tags(cls, v):
        if v is None:
            return None
        return normalize_tags(v)

    class Config:
        extra = "forbid"
