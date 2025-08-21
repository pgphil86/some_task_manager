from enum import Enum


class TaskStatus(str, Enum):
    """
    Статусы задач в системе.

    Attributes:
        CREATED: Задача создана, но не начата.
        IN_PROGRESS: Задача в процессе выполнения.
        COMPLETED: Задача завершена.
    """
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
