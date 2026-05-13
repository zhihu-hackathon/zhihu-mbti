#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
http client
'''

import httpx, logging
from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential, wait_exponential_jitter, retry_if_exception, before_sleep_log
from app.utils.log import get_logger

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
def _is_retryable(exc: BaseException) -> bool:
    """只重试网络错误 & 明确可重试的 HTTP 状态码，跳过所有 4xx 客户端错误"""
    if isinstance(exc, httpx.TransportError):   # 连接超时、断连等网络层错误
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS_CODES
    return False

logger = get_logger(__name__)

# ── 统一 retry 策略（含 jitter 防惊群）────────────────────────────
_retry_policy = dict(
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=16, jitter=2),  # ← 关键：加随机抖动
    retry=retry_if_exception(_is_retryable),
    before_sleep=before_sleep_log(logger, logging.WARNING),     # ← 重试时自动打日志
    reraise=True,   # 耗尽次数后抛出原始异常，而非 tenacity 包装异常
)

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
    
    @retry(**_retry_policy)
    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.get(url=path.lstrip('/'), params=params)
        resp.raise_for_status()
        return resp.json()
    
    @retry(**_retry_policy)
    async def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.post(url=path.lstrip('/'), json=json)
        resp.raise_for_status()
        return resp.json()
    
    @retry(**_retry_policy)
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

    @retry(**_retry_policy)
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.get(url=path.lstrip('/'), params=params)
        resp.raise_for_status()
        return resp.json()

    @retry(**_retry_policy)
    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.post(url=path.lstrip('/'), json=json)
        resp.raise_for_status()
        return resp.json()

    @retry(**_retry_policy)
    def post_data(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.post(url=path.lstrip('/'), data=json)
        resp.raise_for_status()
        return resp.json()