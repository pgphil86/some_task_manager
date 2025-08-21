from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.enum import TaskStatus
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate, TaskStatus as DTOStatus

STATUS_MAP = {
    DTOStatus.created: TaskStatus.CREATED,
    DTOStatus.in_progress: TaskStatus.IN_PROGRESS,
    DTOStatus.completed: TaskStatus.COMPLETED,
}


class TaskCRUD:
    """
    CRUD операция для управления задачами в БД.
    """

    @staticmethod
    def create(db: Session, data: TaskCreate) -> Task:
        """
        Создание новой задачи в БД.

        Args:
            db: Сессия бд.
            data: Данные для создания задачи.

        Returns:
            Task: Созданный объект задачи.

        Note:
            Если статус не указан, то ставится по умолчанию.
        """
        status = STATUS_MAP.get(
            data.status,
            TaskStatus.CREATED,
        ) if data.status else TaskStatus.CREATED
        obj = Task(
            title=data.title,
            description=data.description,
            status=status,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, task_id: UUID) -> Task | None:
        """
        Получает задачу по её UUID.

        Args:
            db: Сессия бд.
            task_id: UUID идентификатор задачи.

        Returns:
            Task | None: Объект задачи или None.
        """
        return db.get(Task, task_id)

    @staticmethod
    def get_list(
        db: Session,
        *,
        status: DTOStatus | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[list[Task], int]:
        """
        Получаем список задач с пагинацией и фильтрацией по статусу.

        Args:
            db: Сессия бд.
            status: Фильтр по статусу.
            limit: Максимальное количество задач.
            offset: Смещение для пагинации.

        Returns:
            tuple[list[Task], int]: Список задач и количество.

        Notes:
            Возвращает все задачи если статус не указан.
        """
        stmt = select(Task)
        if status:
            stmt = stmt.where(Task.status == STATUS_MAP[status])
        total = db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = db.execute(
            stmt.order_by(Task.id).limit(limit).offset(offset)
        ).scalars().all()
        return rows, total

    @staticmethod
    def update(db: Session, task_id: UUID, data: TaskUpdate) -> Task | None:
        """
        Обновление задачи в БД.

        Args:
            db: Сессия бд.
            task_id: UUID задачи для обновления.
            data: Данные для обновления задачи.

        Returns:
            Task | None: Обновленный объект задачи или None.

        Note:
            Обновление затрагивает только переданные поля.
        """
        obj = db.get(Task, task_id)
        if not obj:
            return None
        if data.title is not None:
            obj.title = data.title
        if data.description is not None:
            obj.description = data.description
        if data.status is not None:
            obj.status = STATUS_MAP[data.status]
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, task_id: UUID) -> bool:
        """
        Удаляет задачу по её UUID.

        Args:
            db: Сессия бд.
            task_id: UUID задачи для удаления.

        Returns:
            bool: True если задача удалена. False если не найдена.
        """
        obj = db.get(Task, task_id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
