#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
db test
'''

import copy
from fastapi import Request
from fastapi.routing import APIRouter
from app.utils.log import get_logger
from app.api.deps import DBSessionDep
from app.db.user import User
from app.models.user import UserReq
from sqlmodel import select

logger = get_logger(__name__)

router = APIRouter(
    prefix='/db',
    tags=['DB']
)

@router.get(
    path="/users",
    summary="get all user data"
)
async def list_users(db_session: DBSessionDep) -> list[User]:
    """获取所有用户树据"""
    return db_session.exec(select(User)).all()

@router.post(
    path='/users',
    summary='create user',
    response_model_exclude_none=True
)
async def create_user(db_session: DBSessionDep, params: UserReq):
    user = copy.deepcopy(params)
    db_session.add(user)
    db_session.commit()
    db_session.refresh()
    return {'status': 'ok'}