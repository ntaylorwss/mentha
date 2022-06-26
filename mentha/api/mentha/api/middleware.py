import json
import logging
import time
from typing import Any, Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from starlette.types import Message

IRRELEVANT_PATHS = ["/favicon.ico", "/openapi.json", "/docs"]


# https://github.com/tiangolo/fastapi/issues/394#issuecomment-927272627
class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.logger = logging.getLogger("LoggingMiddleware")

    def log_to_stdout(
        self,
        *,
        route: str,
        method: str,
        request_body: dict[str, Any],
        response_body: dict[str, Any],
        status_code: int,
        duration: int,
    ) -> None:
        self.logger.info(
            {
                "method": method,
                "route": route,
                "status_code": status_code,
                "duration": duration,
                "request_body": request_body,
                "response_body": response_body,
            }
        )

    async def log_request_and_response(
        self,
        *,
        request: Request,
        response: StreamingResponse,
        start_time: float,
        method: str,
    ) -> None:
        request_body = await request.json() if method == "POST" else {}
        duration = int((time.time() - start_time) * 1000)
        response_body_sections = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body_sections))
        response_body = json.loads(response_body_sections[0].decode())

        self.log_to_stdout(
            method=request.method,
            route=request["path"],
            request_body=request_body,
            response_body=response_body,
            status_code=response.status_code,
            duration=duration,
        )

    async def set_body(self, request: Request) -> None:
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    # https://github.com/encode/starlette/issues/874#issuecomment-1027743996
    # we ignore the type here because we're breaking the contract by calling the return type of
    # call_next Awaitable[StreamingResponse] instead of Awaitable[Response], but that is what it is
    # in all cases for our API, so this is fine
    async def dispatch(  # type: ignore
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[StreamingResponse]],
    ) -> Response:
        start_time = time.time()

        await self.set_body(request)

        response = await call_next(request)

        if request["path"] not in IRRELEVANT_PATHS:
            await self.log_request_and_response(
                request=request,
                response=response,
                start_time=start_time,
                method=request.method,
            )

        return response
