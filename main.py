from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
import uvicorn

from core.logging import configure_logging
from api.v1.task import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager для управления жизненным циклом приложения.

    Args:
        app: FastAPI приложение.

    Yields:
        None: Контекст выполнения приложения.
    """
    configure_logging()
    logger.info("Приложение запускается.")
    logger.info("Logging configured запущен успешно.")
    try:
        yield
    finally:
        logger.info("Приложение останавливается.")
        logger.info("Очистка успешна.")


app = FastAPI(
    title="Some Task Manager API.",
    description="CRUD API для управления задачами.",
    version="0.0.1"
)

app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    """
    Проверка здоровья приложения.

    Returns:
        dict: Статус приложения.
    """
    logger.info("Проверка здоровья пройдена.")
    return {"status": "healthy", "service": "some_task_manager"}


@app.get("/")
async def root():
    """
    Корневой endpoint API.

    Returns:
        dict: Информация о API и ссылки на документацию.
    """
    return {
        "message": "Some Task Manager API",
        "version": "0.0.1",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/info")
async def api_info():
    """
    Информация о API.

    Returns:
        dict: Детальная информация о сервисе.
    """
    logger.debug("Запрос информации о API.")
    return {
        "service": "some_task_manager",
        "version": "0.0.1",
        "description": "CRUD API для управления задачами.",
        "endpoints": {
            "tasks": "/api/v1/tasks",
            "health": "/health",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    """
    Точка входа для запуска сервера разработки.
    """
    logger.info("Запуск сервера на http://0.0.0.0:8000.")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
