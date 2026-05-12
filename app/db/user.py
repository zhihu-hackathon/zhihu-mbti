#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlmodel import Field, SQLModel
from typing import Annotated
from datetime import datetime
from datetime import timezone

class User(SQLModel, table=True):
    '''
    table: user
    '''
    __tablename__ = 'user'

    id: Annotated[int | None, Field(default=None, primary_key=True)]

    create_time: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]
    update_time: Annotated[datetime | None, Field(default=None)]