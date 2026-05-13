#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
db test
'''

from fastapi import Request
from fastapi.routing import APIRouter
from app.utils.log import get_logger
from app.api.deps import DBSessionDep
from app.db.user import User
from app.models.user import UserReq
from sqlmodel import select, delete

logger = get_logger(__name__)

router = APIRouter(
    prefix='/db',
    tags=['DB']
)

@router.get(
    path="/users",
    summary="get all user data",
    response_model_exclude_none=True
)
async def list_users(db_session: DBSessionDep) -> list[User]:
    """获取所有用户数据"""
    return db_session.exec(select(User)).all()

@router.post(
    path='/users',
    summary='create user',
    response_model_exclude_none=True
)
async def create_user(db_session: DBSessionDep, params: UserReq):
    '''
    创建测试用户
    '''
    user = User(**params.__dict__)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return {'status': 'ok'}

@router.delete(
    path="/users",
    summary='删除',
    response_model_exclude_none=True
)
async def delete_users(db_session: DBSessionDep):
    '''
    删除所有用户
    '''
    db_session.exec(delete(User))
    db_session.commit()
    return {'status': 'ok'}

@router.delete(
    path="/drop",
    summary='删除整个db',
    response_model_exclude_none=True
)
async def drop_db(request: Request):
    sql_path = request.app.state.sql_path
    sql_path.unlink(missing_ok=True)
    return {'status': 'ok'}