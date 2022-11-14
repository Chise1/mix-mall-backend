from datetime import timedelta
from typing import Optional

from fast_tmp.conf import settings
from fast_tmp.utils.token import decode_access_token, create_access_token
from fastapi import HTTPException, Header
from jose import JWTError
from starlette import status

from fast_store_backend.models import Customer

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_token(customer: Customer) -> str:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": customer.pk}, expires_delta=access_token_expires
    )
    return  access_token


async def get_customer(token: str = Header(...)):
    try:
        payload = decode_access_token(token)
        pk: str = payload.get("id")
        if pk is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    customer = await Customer.filter(pk=pk).first()
    if customer is None:
        raise credentials_exception
    return customer


async def get_customer_or_none(token: Optional[str] = Header(...)) -> Optional[Customer]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        pk: str = payload.get("id")
        if pk is None:
            return None
    except JWTError:
        return None
    return await Customer.filter(pk=pk).first()
