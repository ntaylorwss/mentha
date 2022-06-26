from fastapi import Depends
from pydantic import BaseModel
from scraper.router import router


class Request(BaseModel):
    a: str
    b: int
    c: float


class Response(BaseModel):
    d: float


@router.get("/placeholder", response_model=Response)
async def placeholder(request: Request = Depends()) -> Response:
    return Response(d=len(request.a) + request.b + request.c)
