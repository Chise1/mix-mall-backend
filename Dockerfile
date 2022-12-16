FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim-2022-12-12
MAINTAINER Chise1
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip3 install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN mkdir -p /app
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install
COPY ./src /app
