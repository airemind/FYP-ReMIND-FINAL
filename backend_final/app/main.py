from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.config.settings import settings
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
from app.tasks.scheduler import start_scheduler
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.user_routes import router as user_router
from app.api.routes.admin_routes import router as admin_router
from app.api.routes.chat_routes import router as chat_router
from app.api.routes.message_routes import router as message_router
from app.api.routes.profile_routes import router as profile_router
from app.api.routes.image_ai_routes import router as image_ai_router
from app.api.routes.image_processing_routes import router as image_processing_router
from app.api.routes.text_processing_routes import router as text_processing_router
from app.api.routes.voice_processing_routes import router as voice_processing_router
from app.api.routes.memory_routes import router as memory_router
from app.logs.request_logger import request_logger
from app.middleware.request_middleware import RequestLoggingMiddleware
from app.middleware.security_middleware import SecurityHeadersMiddleware
from app.middleware.cors_middleware import setup_cors

app = FastAPI(title=settings.APP_NAME)

setup_cors(app)
start_scheduler()

request_logger.info("ReMIND backend started successfully")

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(profile_router)
app.include_router(image_ai_router)
app.include_router(image_processing_router)
app.include_router(text_processing_router)
app.include_router(voice_processing_router)
app.include_router(memory_router)


@app.get("/")
def root():

    return {"message": "ReMIND Backend Running"}
