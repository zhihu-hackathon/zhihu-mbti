#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pydantic import BaseModel, Field
from typing import Annotated

class UserReq(BaseModel):
    uid: Annotated[int | None, Field(default=None)]
    fullname: Annotated[str | None, Field(default=None)]
    gender: Annotated[str | None, Field(default=None)]
    headline: Annotated[str | None, Field(default=None)]
    description: Annotated[str | None, Field(default=None)]
    avatar_path: Annotated[str | None, Field(default=None)]
    phone_no: Annotated[str | None, Field(default=None)]
    email: Annotated[str | None, Field(default=None)]
    tag: Annotated[str | None, Field(default=None)]