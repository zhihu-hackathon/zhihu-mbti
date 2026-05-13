#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlmodel import Session, select
from app.db.user import User
from typing import Annotated
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
    SESSION_STORE = request.app.state.session_store
    session_id = request.cookies.get('session_id')
    if not session_id or session_id not in SESSION_STORE:
        return None
    user_id = SESSION_STORE[session_id]
    # get user form db
    user = db_session.exec(select(User).where(User.uid == user_id)).first()
    if not user:
        return None
    return user
# curr user dep
CurrUserDep = Annotated[User, Depends(get_curr_user)]