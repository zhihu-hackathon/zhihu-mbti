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
    uid: Annotated[int | None, Field(nullable=True)]
    fullname: Annotated[str | None, Field(nullable=True)]
    gender: Annotated[str | None, Field(nullable=True)]
    headline: Annotated[str | None, Field(nullable=True)]
    description: Annotated[str | None, Field(nullable=True)]
    avatar_path: Annotated[str | None, Field(nullable=True)]
    phone_no: Annotated[str | None, Field(nullable=True)]
    email: Annotated[str | None, Field(nullable=True)]
    access_token: Annotated[str | None, Field(nullable=True)]
    tag: Annotated[str | None, Field(nullable=True)]
    create_time: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]
    update_time: Annotated[datetime | None, Field(default=None)]