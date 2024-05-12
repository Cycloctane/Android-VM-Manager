from typing import Optional
from fastapi import APIRouter, Request, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
import redis.asyncio as redis

from ...db import redis_pool
from ..utils import is_mac_address
from ..model import Message


router = APIRouter(tags=["Client"], default_response_class=ORJSONResponse)


@router.post("/signin")
async def signin(request: Request, mac: Optional[str] = Form()) -> Message:
    if mac is None or not is_mac_address(mac) or request.client is None:
        raise HTTPException(status_code=400, detail="bad request")
    client_ip: str = request.client.host
    async with redis.Redis.from_pool(redis_pool) as redis_conn:
        await redis_conn.set(f"ip:{mac.replace(':', '-')}", client_ip)
    return Message(msg="success")
