FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim-2022-12-12 
MAINTAINER Chise1
ENV POETRY_VIRTUALENVS_CREATE=false 
RUN pip3 install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple # 我是用了poetry管理环境，所以要单独安装这个
RUN mkdir -p /app # 这是固定的
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install # 类似于pip install -r requirements.txt
COPY ./src /app
