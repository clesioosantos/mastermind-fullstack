from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import AppException
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.games import router as games_router


app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "status_code": exc.status_code,
        },
    )


app.include_router(auth_router, prefix="/api")
app.include_router(games_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Mastermind API is running"}
