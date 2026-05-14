#!/usr/bin/env python
#-*- coding:utf-8 -*-

from app.utils.log import get_logger
from fastapi.routing import APIRouter
from app.api.deps import DBSessionDep, CurrUserDep

logger = get_logger(__name__)

router = APIRouter(
    prefix="/quiz",
    tags=['Quiz']
)

@router.get(
    path="/",
    summary='get quiz result',
    response_model_exclude_none=True
)
def get_res():
    pass


@router.post(
    path="/",
    summary='create quiz',
    response_model_exclude_none=True
)
def create_quiz(curr_user: CurrUserDep):
    
    pass
