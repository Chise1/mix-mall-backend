FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-2022-12-12
MAINTAINER Chise1
ENV POETRY_VIRTUALENVS_CREATE=false
RUN mkdir -p /app
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install
COPY ./src /app
