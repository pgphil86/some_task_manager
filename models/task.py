from uuid import uuid4

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.enum import TaskStatus
from db.base import Base


class Task(Base):
    """
    Модель задачи в системе.

    Представляет собой задачу с уникальным идентификатором,
    названием, описанием и статусом выполнения.
    Наследование идёт от базовой модели sqlalchemy.

    Attributes:
        id: UUID идентификатор задачи (первичный ключ).
        title: Название задачи (обязательно, до 100 символов).
        desctription: Описание задачи (опционально, до 500 символов).
        status: Статус выполнения задач (из enum TaskStatus).
    """
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        name="task_status",
        default=TaskStatus.CREATED,
        nullable=False,
    )
