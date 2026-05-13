#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
auth router
'''

import os, secrets
from fastapi.routing import APIRouter
from fastapi import Request, Response
from app.api.deps import DBSessionDep
from app.utils.http_client import AsyncHttpClient
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.db.user import User
from app.utils.log import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/oauth",
    tags=["Auth"]
)

@router.get(
    path="/callback",
    summary="oauth callback"
)
async def callback(request: Request, authorization_code: str, db_session: DBSessionDep, response: Response):
    '''
    handle oauth callback
    '''
    if not authorization_code:
        return RedirectResponse("/")
    SESSION_STORE = request.app.state.session_store
    session_id = request.cookies.get('session_id')
    if not session_id or session_id not in SESSION_STORE:
        # logined
        return RedirectResponse("/")
    # get access token
    base_url = os.environ.get('ZHIHU_BASE_URL')
    app_id = os.environ.get('ZHIHU_CLIENT_ID')
    app_key = os.environ.get('ZHIHU_CLIENT_SECRET')
    redirect_uri = f'{base_url}/api/oauth/callback'
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
    async with AsyncHttpClient(
        base_url=base_url,
        headers=headers
    ) as client:
        resp = await client.post(path='/access_token', json=request_body)
        if 'access_token' in resp:
            access_token = resp['access_token']
            expires_in = resp['expires_in']
        else:
            logger.error(f"get access token failed with code: {resp['code']} and data: {resp['data']}")
    if not access_token or not expires_in:
        return RedirectResponse('/')
    else:
        # use token to get user info
        # write to db
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        async with AsyncHttpClient(
            base_url=base_url,
            headers=headers
        ) as client:
            resp = await client.get(path='/user')
            if 'code' in resp or 'data' in resp:
                logger.error(f"get user info failed with code: {resp['code']} and data: {resp['data']}")
                return RedirectResponse('/')
            uid = user['uid']
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
                    email=resp['email']
                )
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)

        session_id = secrets.token_urlsafe(32)
        SESSION_STORE[session_id] = user.uid
        # save to cookie
        response.set_cookie(
            key='session_id',
            value=session_id,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=expires_in
        )
        return RedirectResponse('/')

@router.post(
    path="/logout",
    summary="logout"
)
async def logout(request: Request, response: Response):
    """logout"""
    # delete data in session
    session_id = request.cookies.get("session_id")
    if not session_id:
        SESSION_STORE = request.app.state.session_store
        SESSION_STORE.pop(session_id, None)
        response.delete_cookie("session_id")
    return RedirectResponse('/')