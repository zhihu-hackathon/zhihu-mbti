#!/usr/bin/env python
#-*- coding:utf-8 -*-

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlmodel import create_engine
from app.api.routers import db, auth
from sqlmodel import SQLModel
from pathlib import Path
from app.utils.log import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):


    db_path = Path(__file__).parents[1].joinpath('data')
    if db_path is None:
        logger.info(f'{db_path} not set use the default db path')
        if not db_path.exists():
            db_path.mkdir(parents=True)
    else:
        logger.info(f'{str(db_path)} exist')
    sql_path = str(db_path.joinpath('database.db'))

    # init db
    sql_url = f'sqlite:///{sql_path}'
    sql_engine = create_engine(sql_url, echo=True)
    app.state.sql_engine = sql_engine
    # init db
    SQLModel.metadata.create_all(sql_engine)

    try:
        yield
    finally:
        pass

app = FastAPI(title='zhihu-mbti', summary='zhihu mbti', version='1.0', lifespan=lifespan)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(db.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def default_exception_handler(request, exc: Exception):
    '''
    handler do not handle request error(401, 403 .etc)
    HttpException will not handle too
    just handle the uncaught exceptions
    '''
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'server error please try again'}
    )