#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlmodel import Session
from typing import Annotated
from fastapi import Depends, Request

# db session function
async def get_session(request: Request):
    engine = request.app.sql_engine
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# db session deps
DBSessionDep = Annotated[Session, Depends(get_session)]