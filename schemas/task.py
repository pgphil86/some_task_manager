from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    """
    Базовая схема задачи для валидации полей.

    Содержит общие поля для создания и ообновления задач.
    """
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи.

    Наследует базовые поля и добавляет опциональный статус.
    Если его нет, то устанавливается значение по умолчанию.
    """
    status: TaskStatus | None = None


class TaskUpdate(BaseModel):
    """
    Схема для обновления существующей задачи.

    Все поля опциональны.
    Обновляется название, описание и статус.
    """
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None


class TaskRead(TaskBase):
    """
    Схема для чтения данных задачи.

    Содержит все поля задачи включая ID и статус.
    """
    id: UUID
    status: TaskStatus
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    """
    Схема для возврата списка задач с пагинацией.

    Содержит массив задач и общее количество для пагинации.
    """
    items: list[TaskRead]
    total: int
