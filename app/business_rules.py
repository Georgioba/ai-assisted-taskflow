from fastapi import HTTPException, status

from app.models import TaskStatus


VALID_STATUS_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset(
    {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    }
)


def validate_status_transition(
    current_status: TaskStatus,
    new_status: TaskStatus,
) -> None:
    if (current_status, new_status) in VALID_STATUS_TRANSITIONS:
        return

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=(
            "Invalid status transition "
            f"from {current_status.value} to {new_status.value}"
        ),
    )
