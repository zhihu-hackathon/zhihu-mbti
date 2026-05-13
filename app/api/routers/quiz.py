#!/usr/bin/env python
#-*- coding:utf-8 -*-

from app.utils.log import get_logger
from fastapi.routing import APIRouter

logger = get_logger(__name__)

router = APIRouter(
    prefix="/quiz",
    tags=['Quiz']
)

