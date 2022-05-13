import uvicorn
from fastapi import FastAPI

from core.settings import load_settings
from src.api_v1.routers import api_router
from src.db.session import db_session_provider, stub


def main() -> FastAPI:
    fastapi = FastAPI()

    fastapi.include_router(api_router)

    config = load_settings()
    fastapi.dependency_overrides[stub] = db_session_provider(config)

    return fastapi


app = main()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True, log_config='logs/logger.yml')
