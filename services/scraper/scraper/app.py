from fastapi import FastAPI
from scraper.router import router

from mentha.api.middleware import LoggingMiddleware

app = FastAPI()
app.include_router(router)
app.add_middleware(LoggingMiddleware)
