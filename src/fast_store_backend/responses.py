# -*- encoding: utf-8 -*-
"""
@File    : responses.py
@Time    : 2022/10/1 17:23
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :商城默认返回结果
"""
from typing import Any

from pydantic import BaseModel


class StoreRes(BaseModel):
    """
    默认小程序返回结果
    """
    code: str = '0'
    data: Any
