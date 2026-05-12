#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
auth router
'''

from fastapi.routing import APIRouter
from app.api.deps import DBSessionDep

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get(
    path="/test",
    summary="test"
)
async def get_job():
    """根据job id 获取job的详细信息"""
    # 省略具体逻辑
    return 1

# @router.post(
#     path="/login",
#     summary="login with email and password",
#     response_model=LoginRes,
#     response_model_exclude_none=True)
# async def login(param: LoginReq, db_session: DBSessionDep) -> LoginRes:
#     sts = select(User).where(User.email == param.email)
#     user = db_session.exec(sts).first()
#     if not user:
#         return LoginRes(status="failed", message="用户名或密码不对")
#     pw_res = check_pw(param.password, user.password)
#     if not pw_res:
#         return LoginRes(status="failed", message="用户名或密码不对")
#     data = {
#         'sub': str(user.id),
#         'roles': [role.name for role in user.roles],
#         'first_name': user.first_name,
#         'last_name': user.last_name
#     }
#     access_token = create_token(data)
#     return LoginRes(status="ok", access_token=access_token)