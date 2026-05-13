#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
index
'''

from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.utils.log import get_logger
from app.api.deps import DBSessionDep, CurrUserDep

logger = get_logger(__name__)

router = APIRouter(
    prefix="",
    tags=['Index']
)

@router.get(
    path="/",
    response_class=HTMLResponse
)
def home(request: Request, db_session: DBSessionDep, curr_user: CurrUserDep):
    templates = request.app.state.templates
    if not curr_user:
        logger.info('current user not login')
        return templates.TemplateResponse(request=request, name="index.html")
    else:
        # contains user info
        logger.info('user login')
        # render user
        return templates.TemplateResponse(request=request, name="index.html")
