FROM python:3.12-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем проект
COPY . .

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
