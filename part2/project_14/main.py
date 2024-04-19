import os
import re
from pathlib import Path
from typing import Callable

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import config
from src.database.db import get_db
from src.routes import contacts_router, auth_router, users_router

app = FastAPI()

user_agent_ban_list = [r"YandexBot", r"Googlebot"]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    """
    Middleware to ban user agents based on a ban list.

    :param request: The incoming request.
    :type request: Request
    :param call_next: The next middleware function in the chain.
    :type call_next: Callable
    :return: A JSONResponse with a 403 status code if the user agent is banned,
             otherwise the response from the next middleware.
    :rtype: JSONResponse or Response
    """

    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "You are banned"},
            )
    response = await call_next(request)
    return response


BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")
app.mount("/static", StaticFiles(directory=directory), name="static")


app.include_router(auth_router.router, prefix="/api")
app.include_router(users_router.router, prefix="/api")
app.include_router(contacts_router.router, prefix="/api")


@app.on_event("startup")
async def startup():
    """
    Startup event handler for FastAPI application.

    Initializes the Redis connection and FastAPI limiter.
    """

    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")  # noqa


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    Root endpoint that serves the index.html template.

    :param request: The incoming request.
    :type request: Request
    :return: The rendered HTML template for the index page.
    :rtype: HTMLResponse
    """

    return templates.TemplateResponse(
        "index.html", context={"request": request, "our": "Build group WebPython"}
    )


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Healthcheck endpoint that checks the database connection.

    :param db: The database session.
    :type db: AsyncSession
    :raises HTTPException: If there's an error connecting to the database.
    :return: A success message if the database is connected correctly.
    :rtype: dict
    """

    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=int(os.environ.get("PORT", 8000)), reload=True, log_level="info")
