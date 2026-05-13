#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
auth router
'''

import os, secrets
from fastapi.routing import APIRouter
from fastapi import Request, Response
from app.api.deps import DBSessionDep
from app.utils.http_client import SyncHttpClient
from app.db.session import UserSession
from fastapi.responses import RedirectResponse
from sqlmodel import select, update
from app.db.user import User
from app.utils.log import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="",
    tags=["Auth"]
)

@router.get(
    path="/oauth/callback",
    summary="oauth callback"
)
def callback(request: Request, authorization_code: str, db_session: DBSessionDep, response: Response):
    '''
    handle oauth callback
    '''
    if not authorization_code:
        logger.warning('error code not exist')
        return RedirectResponse("/")
    session_id = request.cookies.get('session_id')
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
        # logined
        logger.warning('user logged')
        return RedirectResponse("/")
    # get access token
    base_url = os.environ.get('ZHIHU_BASE_URL')
    app_base_url = os.environ.get('APP_BASE_URL')
    app_id = os.environ.get('ZHIHU_CLIENT_ID')
    app_key = os.environ.get('ZHIHU_CLIENT_SECRET')
    redirect_uri = f'{app_base_url}/api/oauth/callback'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request_body = {
        'app_id': app_id,
        'app_key': app_key,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': authorization_code
    }
    access_token = None
    expires_in = None
    with SyncHttpClient(
        base_url=base_url,
        headers=headers
    ) as client:
        resp = client.post_data(path='/access_token', json=request_body)
        if 'access_token' in resp:
            access_token = resp['access_token']
            expires_in = resp['expires_in']
        else:
            logger.error(f"get access token failed with code: {resp['code']} and data: {resp['data']}")
    if not access_token or not expires_in:
        logger.warning('get access token failed')
        return RedirectResponse('/')
    else:
        # use token to get user info
        # write to db
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        with SyncHttpClient(
            base_url=base_url,
            headers=headers
        ) as client:
            resp = client.get(path='/user')
            if 'code' in resp or 'data' in resp:
                logger.error(f"get user info failed with code: {resp['code']} and data: {resp['data']}")
                return RedirectResponse('/')
            uid = resp['uid']
            # check user in table
            user = db_session.exec(select(User).where(User.uid == uid)).first()
            if not user:
                user = User(
                    uid=resp['uid'],
                    fullname=resp['fullname'],
                    gender=resp['gender'],
                    headline=resp['headline'],
                    description=resp['description'],
                    avatar_path=resp['avatar_path'],
                    phone_no=resp['phone_no'],
                    email=resp['email'],
                    access_token=access_token
                )
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
            else:
                # update user access token
                user.access_token = access_token
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
        session_id = secrets.token_urlsafe(32)
        # upsert the session info
        uid = user.uid
        user_session = db_session.exec(select(UserSession).where(UserSession.uid == uid)).first()
        if user_session:
            user_session.session_id = session_id
            user_session.expires_in = expires_in
        else:
            user_session = UserSession(
                uid=uid,
                session_id=session_id,
                expires_in=expires_in
            )
        db_session.add(user_session)
        db_session.commit()
        # save to cookie
        logger.warning(f'logincallback 写入cookie之前session_id: ${session_id}')
        redirect = RedirectResponse(url='/', status_code=302)
        redirect.set_cookie(
            key='session_id',
            value=session_id,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=expires_in,
            path="/"
        )
        return redirect

@router.post(
    path="/v1/auth/logout",
    summary="logout"
)
def logout(request: Request, response: Response, db_session: DBSessionDep):
    """logout"""
    # delete data in session
    session_id = request.cookies.get("session_id")
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
        # delete session
        logger.warning('logout session is not null')
        db_session.delete(user_session)
        db_session.commit()
    redirect = RedirectResponse(url='/', status_code=302)
    redirect.delete_cookie("session_id")
    return redirect

# get auth status to update front-end
@router.get(
    path="/v1/auth/status",
    summary="check auth status",
    response_model_exclude_none=True
)
def get_auth_status(request: Request, db_session: DBSessionDep):
    session_id = request.cookies.get("session_id")
    logger.warning(f'当前session id is ${session_id}')
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if session_id and user_session:
       # get user info
       logger.warning(f'当前session id is ${session_id} 以及 user session: ${user_session}')
       user = db_session.exec(select(User).where(User.uid == user_session.uid)).first()
       if user:
            return {'auth': True, 'user': {
                'id': user.uid,
                'name': user.fullname,
                'gender': user.gender,
                'headline': user.headline,
                'avatar': user.avatar_path,
                'description': user.description
            }}
       else:
            logger.warning(f'当前user 为空 结果 session id is ${session_id} 以及 user session: ${user_session}')
            return {'auth': False, 'user': None}
    logger.warning(f'当前false结果 session id is ${session_id} 以及 user session: ${user_session}')
    return {'auth': False, 'user': None}