#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlmodel import Session, select
from app.db.user import User
from typing import Annotated
from app.db.session import UserSession
from fastapi import Depends, Request, HTTPException, Response, status

# db session function
async def get_session(request: Request):
    engine = request.app.state.sql_engine
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
# db session dep
DBSessionDep = Annotated[Session, Depends(get_session)]

# get user
async def get_curr_user(request: Request, db_session: DBSessionDep):
    session_id = request.cookies.get('session_id')
    user_session = db_session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if not session_id or not user_session:
        return None
    user_id = user_session.session_id
    # get user form db
    user = db_session.exec(select(User).where(User.uid == user_id)).first()
    if not user:
        return None
    return user
# curr user dep
CurrUserDep = Annotated[User, Depends(get_curr_user)]