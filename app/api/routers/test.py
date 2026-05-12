#!/usr/bin/env python
#-*- coding:utf-8 -*-

from fastapi.routing import APIRouter
from app.utils.log import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix='/tests',
    tags=['tests']
)

@router.get(
    path="/test",
    summary="test"
)
async def get_job():
    """根据job id 获取job的详细信息"""
    # 省略具体逻辑
    return 1

