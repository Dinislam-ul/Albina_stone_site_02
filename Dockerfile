# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем pyproject.toml
COPY pyproject.toml .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir \
    "fastapi>=0.141.1,<0.142.0" \
    "uvicorn>=0.52.4,<0.53.0" \
    "sqlalchemy>=2.0.52,<3.0.0" \
    "pydantic[email]>=2.13.5,<3.0.0" \
    "ruff>=0.16.5,<0.17.0" \
    "alembic>=1.19.1,<2.0.0" \
    "mypy>=2.3.1,<3.0.0" \
    "asyncpg>=0.31.0,<0.32.0" \
    "pydantic-settings>=2.15.0,<3.0.0" \
    "greenlet>=3.5.5,<4.0.0" \
    "python-jose[cryptography]>=3.5.0,<4.0.0" \
    "passlib[bcrypt]>=1.7.4,<2.0.0" \
    "python-multipart>=0.0.32,<0.0.33" \
    "dotenv>=0.9.9,<0.10.0" \
    "bcrypt>=5.0.0,<6.0.0" \
    "boto3>=1.35.0" \
    "celery>=5.3.0" \
    "fastapi-mail>=1.4.1" \
    "redis>=5.0.0" 

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Команда для запуска (будет переопределена в docker-compose)
CMD ["uvicorn", "stone_site.main:app", "--host", "0.0.0.0", "--port", "8000"]