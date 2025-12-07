"""FastAPI application setup for FIO emulator."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fioemu.config import Config


def create_app(config: Config) -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="FIO Banking API Emulator",
        description="Emulator for FIO Banking API v1.9",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=config.cors_allow_credentials,
        allow_methods=config.cors_allow_methods,
        allow_headers=config.cors_allow_headers,
    )

    # Include routers will be done in __main__.py after routers are created
    return app

