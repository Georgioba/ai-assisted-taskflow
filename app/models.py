from enum import Enum
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
        value = value.split(",")
    if not isinstance(value, list):
        raise ValueError("tags must be a list or comma-separated string")

    normalized = []
    for tag in value:
        if not isinstance(tag, str):
            raise ValueError("each tag must be a non-empty string")
        tag_text = tag.strip()
        if not tag_text:
            raise ValueError("tags must not contain empty values")
        if len(tag_text) > 20:
            raise ValueError("each tag must be 20 characters or fewer")
        normalized.append(tag_text)

    if len(normalized) > 5:
        raise ValueError("at most 5 tags are allowed")
    return normalized


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be empty or whitespace")
        return cleaned

    @field_validator("tags", mode="before")
    @classmethod
    def clean_tags(cls, value):
        return normalize_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def title_strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            raise ValueError("title cannot be null")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be empty or whitespace")
        if len(cleaned) > 200:
            raise ValueError("title too long")
        return cleaned

    @field_validator("tags", mode="before")
    @classmethod
    def clean_tags(cls, value):
        if value is None:
            return None
        return normalize_tags(value)
