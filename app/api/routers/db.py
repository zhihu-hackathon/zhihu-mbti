#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
db test
'''

import os, json
from fastapi import Request
from fastapi.routing import APIRouter
from app.utils.log import get_logger
from app.api.deps import DBSessionDep
from app.db.user import User
from app.db.session import UserSession
from app.models.user import UserReq
from sqlmodel import select, delete
from app.utils.http_client import SyncHttpClient

logger = get_logger(__name__)

router = APIRouter(
    prefix='/db',
    tags=['DB']
)

@router.get(
    path="/llm",
    summary='test llm'
)
def test_llm():
    access_token = os.environ.get('USER_ACCESS_TOKEN', '')
    base_url = os.environ.get('ZHIHU_BASE_URL')
    json_str = ''
    with SyncHttpClient(
        base_url=base_url,
        headers={'Authorization': f'Bearer{access_token}'}
    ) as client:
        resp = client.get('/user/moments')
        if 'data' in resp:
            json_str = json.dumps(resp['data'])
    print(json_str)
    return {'status': 'ok'}

@router.get(
    path="/users",
    summary="get all user data",
    response_model_exclude_none=True
)
def list_users(db_session: DBSessionDep) -> list[User]:
    """获取所有用户数据"""
    return db_session.exec(select(User)).all()

@router.post(
    path='/users',
    summary='create user',
    response_model_exclude_none=True
)
def create_user(db_session: DBSessionDep, params: UserReq):
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
def delete_users(db_session: DBSessionDep):
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
def drop_db(request: Request):
    sql_path = request.app.state.sql_path
    sql_path.unlink(missing_ok=True)
    return {'status': 'ok'}


@router.get(
    path="/user-sessions",
    summary="获取所有user sessions",
    response_model_exclude_none=True
)
def get_user_sessions(db_session: DBSessionDep):
    return db_session.exec(select(UserSession)).all()

@router.delete(
    path="/user-sessions/{id}",
    summary="删除某个session",
    response_model_exclude_none=True
)
def delete_user_session(id: int, db_session: DBSessionDep):
    res = db_session.exec(select(UserSession).where(UserSession.uid == id)).all()
    for item in res:
        db_session.delete(item)
    db_session.commit()
    return {'status': 'ok'}