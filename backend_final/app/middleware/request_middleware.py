import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.logs.request_logger import request_logger
from app.logs.error_logger import error_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = round(time.time() - start_time, 3)
            request_logger.info(
                f"{request.method} "
                f"{request.url.path} "
                f"STATUS={response.status_code} "
                f"TIME={process_time}s"
            )

            return response

        except Exception as e:
            error_logger.error(
                f"{request.method} " f"{request.url.path} " f"ERROR={str(e)}"
            )
            raise e
