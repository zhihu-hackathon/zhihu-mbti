#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import create_engine
from app.api.routers import test, auth
from pathlib import Path
from app.utils.log import get_logger

logger = get_logger(__name__)

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

    db_path = Path(__file__).parents[1].joinpath('data')
    if db_path is None:
        logger.info(f'{db_path} not set use the default db path')
        if not db_path.exists():
            db_path.mkdir(parents=True)
    else:
        logger.info(f'{str(db_path)} exist')
    
    # init db

    try:
        yield
    finally:
        pass

app = FastAPI(title='zhihu-mbti', summary='zhihu mbti', version='1.0', lifespan=lifespan)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(test.router, prefix="/api/v1")