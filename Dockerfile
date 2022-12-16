FROM python:3.8-slim
ENV POETRY_VIRTUALENVS_CREATE=false
RUN mkdir -p /src
WORKDIR /src
RUN pip3 install -i poetry  https://pypi.tuna.tsinghua.edu.cn/simple
COPY pyproject.toml poetry.lock /src/
RUN poetry install
COPY ./src /src
