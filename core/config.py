import os
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """
    Конфигурационные настройки приложения Task Manager API.

    Класс отвечает за загрузку  и валидацию настроек из переменных окружения
    с представлением значений по умолчанию (для разработки).

    Attributes:
        app_name (str): Название приложения для идентификации.
        env (Literal): Среда выполнения окружения (dev, prod, test).
        log_level (Literal): Уровень детализация логирования.
        log_dir (str): Директория для хранения файлов логирования.
        database_url (url): URL для подключения к БД.

    Features:
        - Автоматическая загрузка из переменных окружения.
        - Валидация типов и значений.
        - Автоматическое создание необходимых директорий.
        - Подробное описание для каждой настройки.

    Environment Variables:
        APP_NAME: Название приложения (default: "some_task_manager").
        ENV: Среда выполнения (default: "dev").
        LOG_LEVEL: Уровень логирования (default: "INFO).
        LOG_DIR: Путь к директории логов (default: "logs").
        DATABASE_URL: URL для подключения к БД.

    Note:
        Для prod среды рекомендуется явно задавать все переменные окружения.
        Значения по умолчанию предназначены для dev, test.
    """
    app_name: str = Field(
        default=os.getenv(
            "APP_NAME",
            "some_task_manager"
        ),
        description=os.getenv(
            "APP_NAME_DESCRIPTION",
            "Название приложения для идентификации."
        ),
    )
    env: Literal["dev", "prod", "test"] = Field(
        default=os.getenv("ENV", "dev"),
        description=os.getenv("ENV_DESCRIPTION", "Среда выполнения."),
    )
    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description=os.getenv(
            "LOG_LEVEL_DESCRIPTION",
            "Уровень детализации логов."
        ),
    )
    log_dir: str = Field(
        default=os.getenv("LOG_DIR", "logs"),
        description=os.getenv(
            "LOG_DIR_DESCRIPTION",
            "Директория для хранения файлов с логами."
        ),
    )
    database_url: str = Field(
        default=os.getenv(
            "DATABASE_URL",
        ),
        description=os.getenv(
            "DATABASE_URL_DESCRTION", "URL для подключения к БД."
        ),
    )

    model_config = ConfigDict(
        validate_assignment=True,
        case_sensitive=False,
        frozen=False,
        extra="forbid",
        validate_default=True,
    )

    @field_validator("log_level")
    def validate_log_level(cls, valid_lev):
        """
        Функция для проверки уровня логирования.
        """
        if valid_lev not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(os.getenv("LOG_LEVEL_ERROR"), valid_lev)
        return valid_lev

    @field_validator("log_dir")
    def create_log_dir(cls, valid_dir):
        """
        Функция для проверки существования директории для логов и создания её.
        """
        os.makedirs(valid_dir, exist_ok=True)
        return valid_dir


settings = Settings()
