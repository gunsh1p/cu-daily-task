FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN [ "pip", "install", "-r", "requirements.txt" ]

COPY bot /app
COPY config.py /app/config.py
COPY db /app/db
COPY utils /app/utils
COPY migrations /app/migrations
COPY pyproject.toml /app/pyproject.toml

ENTRYPOINT [ "bash", "-c", "aerich upgrade; python3 main.py" ]