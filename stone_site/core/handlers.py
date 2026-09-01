from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

def register_exeption_handlers(app: FastAPI) -> None:

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

