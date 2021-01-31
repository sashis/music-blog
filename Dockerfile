FROM python:3.9-slim

WORKDIR /app

ENV POETRY_VERSION=1.1.4 \
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=off \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && apt-get clean \
    && useradd --no-create-home nginx \
    && pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN apt-get install -y gcc libpq-dev \
    && poetry export -f requirements.txt | pip install -r /dev/stdin \
    && apt-get autoremove -y gcc \
    && apt-get clean

EXPOSE 80
VOLUME ["/app_data"]

COPY . .

RUN poetry install --no-interaction --no-ansi \
    && chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
