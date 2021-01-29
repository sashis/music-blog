FROM python:3.9-slim

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev nginx \
    && pip install poetry wheel \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi\
    && apt-get autoremove -y gcc \
    && apt-get clean \
    && useradd --no-create-home nginx
USER nginx
EXPOSE 5000
VOLUME ["/app_data"]
COPY . .
CMD ["uwsgi", "--socket=0.0.0.0:5000", "--protocol=http", "-w", "music_blog:app"]
