#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import create_engine
from app.api.routers import test, auth
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):

    db_user = os.environ.get('DB_USER', 'test')
    db_pass = os.environ.get('DB_PASS', 'test')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = int(os.environ.get('DB_PORT', 3306))
    db_name = os.environ.get('DB_NAME', 'test')
    sql_url = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    sql_engine = create_engine(sql_url, echo=True)

    app.state.sql_engine = sql_engine
    # app.state.dumy_job = DumyJob(executor=thread_pool_executor)
    try:
        yield
    finally:
        pass

app = FastAPI(title='zhihu-mbti', summary='zhihu mbti', version='1.0', lifespan=lifespan)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(test.router, prefix="/api/v1")