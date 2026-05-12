#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from sqlmodel import create_engine
from app.api.routers import test
from pathlib import Path

thread_pool_size = int(os.environ.get('THREAD_POOL_SIZE', 10))

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread_pool_executor = ThreadPoolExecutor(max_workers=thread_pool_size, thread_name_prefix='test')
    db_user = os.environ.get('DB_USER', 'test')
    db_pass = os.environ.get('DB_PASS', 'test')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = int(os.environ.get('DB_PORT', 3306))
    db_name = os.environ.get('DB_NAME', 'test')
    sql_url = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    sql_engine = create_engine(sql_url, echo=True)

    # 测试挂载卷
    test_path = Path('/app/db/test.text')
    if test_path.exists():
        print(f'{test_path} exist should delete')
        test_path.unlink()
    else:
        print(f'{test_path} not exist should create')
        test_path.write_text('abc')


    app.state.thread_pool_executor = thread_pool_executor
    app.state.sql_engine = sql_engine
    try:
        yield
    finally:
        thread_pool_executor.shutdown()

app = FastAPI(title='zhihu-mbti', summary='zhihu mbti', version='1.0', lifespan=lifespan)
app.include_router(test.router, prefix="/api/v1")