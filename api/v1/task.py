import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.logging import configure_logging
from db.session import get_db
from schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskList, TaskStatus
from crud.task import TaskCRUD

configure_logging()
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """
    Создает новую задачу.

    Args:
        payload: Данные для создания задачи.
        db: Сессия базы данных.

    Returns:
        TaskRead: Созданная задача.

    Raises:
        HTTPException: При ошибках валидации данных.
    """
    obj = TaskCRUD.create(db, payload)
    logger.info(
        "Задача создана",
        extra={"task_id": str(obj.id), "task_title": obj.title}
    )
    return TaskRead.model_validate(obj.__dict__)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Получает задачу по ID.

    Args:
        task_id: UUID идентификатор задачи.
        db: Сессия базы данных.

    Returns:
        TaskRead: Найденная задача.

    Raises:
        HTTPException: 404 если задача не найдена.
    """
    obj = TaskCRUD.get(db, task_id)
    if not obj:
        logger.warning(
            "Задача не найдена",
            extra={"task_id": str(task_id)}
        )
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    return TaskRead.model_validate(obj)


@router.get("/", response_model=TaskList)
def list_tasks(
    status: TaskStatus | None = Query(
        default=None, description="Фильтр по статусу."
    ),
    limit: int = Query(50, ge=1, le=1000, description="Лимит записей."),
    offset: int = Query(0, ge=0, description="Смещение."),
    db: Session = Depends(get_db),
):
    """
    Получает список задач с пагинацией и фильтрацией.

    Args:
        status: Фильтр по статусу задачи.
        limit: Количество записей на странице.
        offset: Смещение для пагинации.
        db: Сессия бд.

    Returns:
        TaskList: Список задач и общее количество.
    """
    items, total = TaskCRUD.get_list(
        db,
        status=status,
        limit=limit,
        offset=offset,
    )
    logger.debug(
        "Получен список задач.",
        extra={"count": len(items), "total": total, "status": status}
    )
    return TaskList(
        items=[TaskRead.model_validate(item) for item in items],
        total=total
    )


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновляет задачу частично.

    Args:
        task_id: UUID идентификатор задачи.
        payload: Данные для обновления.
        db: Сессия бд.

    Returns:
        TaskRead: Обновленная задача.

    Raises:
        HTTPException: 404 если задача не найдена.
    """
    obj = TaskCRUD.update(db, task_id, payload)
    if not obj:
        logger.warning(
            "Задача не найдена для обновления.",
            extra={"task_id": str(task_id)}
        )
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    logger.info("Задача обновлена.", extra={"task_id": str(task_id)})
    return TaskRead.model_validate(obj)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Удаляет задачу.

    Args:
        task_id: UUID идентификатор задачи.
        db: Сессия бд.

    Returns:
        None: Пустой ответ со статусом 204.

    Raises:
        HTTPException: 404 если задача не найдена.
    """
    ok = TaskCRUD.delete(db, task_id)
    if not ok:
        logger.warning(
            "Задача не найдена для удаления.",
            extra={"task_id": str(task_id)}
        )
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    logger.info("Задача удаленаю", extra={"task_id": str(task_id)})
    return None
