#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlmodel import Field, SQLModel
from typing import Annotated
from datetime import datetime
from datetime import timezone

class UserSession(SQLModel, table=True):
    '''
    table: user_session
    '''
    __tablename__ = 'user_session'

    id: Annotated[int | None, Field(default=None, primary_key=True)]
    uid: Annotated[int, Field(nullable=False)]
    session_id: Annotated[str, Field(nullable=False)]
    expires_in: Annotated[int, Field(nullable=False)]
    create_time: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]
    update_time: Annotated[datetime | None, Field(default=None)]