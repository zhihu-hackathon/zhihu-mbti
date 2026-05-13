#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
http client
'''

import httpx
from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential

class AsyncHttpClient:

    def __init__(
        self,
        base_url,
        timeout: float = 30.0,
        headers: dict[str, Any] | None = None
    ):
        self.base_url = base_url.rstrip('/') + '/'
        self.timeout = timeout
        self.headers = headers or {}
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers
        )
    
    async def __aenter__(self):
        await self._client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
    
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.get(url=path.lstrip('/'), params=params)
        resp.raise_for_status()
        return resp.json()
    
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    async def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.post(url=path.lstrip('/'), json=json)
        resp.raise_for_status()
        return resp.json()
    
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    async def post_data(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.post(url=path.lstrip('/'), data=json)
        resp.raise_for_status()
        return resp.json()

class SyncHttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, Any] | None = None
    ):
        self.base_url = base_url.rstrip('/') + '/'
        self.timeout = timeout
        self.headers = headers or {}
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers
        )

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.__exit__(exc_type, exc_val, exc_tb)

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.get(url=path.lstrip('/'), params=params)
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.post(url=path.lstrip('/'), json=json)
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
    def post_data(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.post(url=path.lstrip('/'), data=json)
        resp.raise_for_status()
        return resp.json()