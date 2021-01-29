FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y gcc libpq-dev nginx \
    && useradd --no-create-home nginx \
    && apt-get clean
WORKDIR /app
COPY ./app .
RUN pip install .
USER nginx
EXPOSE 5000
VOLUME ["/app/instance/"]
CMD ["uwsgi", "--socket=0.0.0.0:5000", "--protocol=http", "-w", "music_blog:app"]
