# -*- encoding: utf-8 -*-
"""
@File    : auth.py
@Time    : 2022/10/2 12:55
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

router = APIRouter(prefix="/user")


class LoginInfo(BaseModel):
    mobile: str
    password: str


@router.post("/sign_in")
async def sigin_in(logininfo: LoginInfo):
    """
    登录
    :param logininfo:
    :return:
    """
    return {
        "token": 'asdfgvaefgasfdg'
    }


@router.get("/addresses")
async def get_address():
    return [
        {
            "id": 1,
            "name": '刘晓晓',
            "mobile": '18666666666',
            "addressName": '贵族皇仕牛排(东城店)',
            "address": '北京市东城区',
            "area": 'B区',
            "default": True
        },
        {
            "id": 2,
            "name": '刘晓晓',
            "mobile": '18666666666',
            "addressName": '贵族皇仕牛排(东城店)',
            "address": '北京市东城区',
            "area": 'B区',
            "default": True
        }
    ]


class CreateAddress(BaseModel):
    id: Optional[int]=None
    name: str
    mobile: str
    address: str
    defalut: bool = False


@router.post("/address")
async def create_address(info: CreateAddress):
    return info


@router.get("/userInfo")
async def userinfo(request: Request):
    return {
        "id": 1,
        "mobile": 18888888888,
        "nickname": 'Leo yo',
        "portrait": 'http://img.61ef.cn/news/201409/28/2014092805595807.jpg'
    }
