from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.records.criminal_complaint_form_records import ccf_record_router
from app.api.api_v1.routers.tasks import task_router
from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.uploads import uploads_router
from app.api.api_v1.routers.auth import auth_router
from app.core import config
from app.core.security import user_over_rate_limit
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user, get_current_active_county_authorized

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(user_over_rate_limit), Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])

# CCF Records Router
app.include_router(
    ccf_record_router,
    prefix="/api/v1/records",
    tags=["records"],
    dependencies=[Depends(get_current_active_county_authorized)]
)

# Task status router
app.include_router(
    task_router,
    prefix="/api/v1",
    tags=["tasks"],
    dependencies=[Depends(get_current_active_county_authorized)]
)

# Uploads router
app.include_router(
    uploads_router,
    tags=["uploads"],
    prefix="/api/v1/uploads",
    dependencies=[Depends(get_current_active_county_authorized), Depends(user_over_rate_limit)]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
