from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

react_main_url = settings.REACT_BASE_URL
react_alternative_url = settings.REACT_BASE_URL_ALTERNATIVE


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[react_main_url, react_alternative_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
