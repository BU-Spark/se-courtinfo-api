from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.uploads import uploads_router
from app.api.api_v1.routers.auth import auth_router
from app.core import config
from app.core.security import user_over_rate_limit
from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
from app.core.celery_app import celery_app

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


# @app.middleware("http")
# async def rate_limit_middleware(request: Request, call_next):
#     client = get_redis_client()
#     if over_limit_multi(client, request):
#         print("stop")
#     response = await call_next(request)
#     return response


@app.get("/api/v1")
async def root():
    db = SessionLocal()
    create_user(
        db,
        UserCreate(
            email="admin@scda-api.org",
            password="password",
            is_active=True,
            is_superuser=True,
        ),
    )
    return {"message": "Hello World"}


@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])
    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(user_over_rate_limit), Depends(get_current_active_user), ],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])

# Uploads router
app.include_router(
    uploads_router,
    prefix="/api/v1/uploads",
    dependencies=[Depends(get_current_active_user), Depends(user_over_rate_limit)]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
