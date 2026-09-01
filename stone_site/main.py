from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from stone_site.core.database import engine, Base
from stone_site.routers.stones import stone_router
from sqlalchemy.exc import SQLAlchemyError
from stone_site.routers.auth import auth_router
from stone_site.core.handlers import register_exeption_handlers

app = FastAPI(title="Stone Site API", description="API platform about stones", version="0.1.0")

register_exeption_handlers(app)

app.include_router(stone_router)       # /stone
app.include_router(auth_router) 

# ----корневая ручка -----
@app.get("startup", tags=["Settings"], summary="Create table in DB")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --------Настройки ----
@app.get("/", tags=["Default"])
async def root():
    return {"message":"Hello. This is Stone Site API"}


@app.get("/health", tags=["Default"])
async def health_check():
    return {"status":"OK"}


# ------Отлавливаем ошибки----------
@app.exception_handler(HTTPException)
async def http_exeption_handler(request: Request, exc: HTTPException):
    return JSONResponse (
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),  
            "path": request.url.path
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_errror_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "error":"Database error",
            "details": "An error occurred while processing your request"
        }
    )

