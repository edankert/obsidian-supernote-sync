"""
FastAPI server for Obsidian-Supernote Sync.

This module provides the main FastAPI application and server startup logic.
It serves as the backend for both the Obsidian plugin and web dashboard.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from obsidian_supernote.api.routes import convert, status, workflows
from obsidian_supernote.api.websocket import manager as ws_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Version info
API_VERSION = "0.1.0"
APP_NAME = "Obsidian-Supernote Sync API"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle startup and shutdown events."""
    # Startup
    logger.info(f"Starting {APP_NAME} v{API_VERSION}")
    # Set start time for uptime tracking
    from obsidian_supernote.api.routes.status import set_start_time
    set_start_time()
    yield
    # Shutdown
    logger.info(f"Shutting down {APP_NAME}")


def create_app(
    dashboard_path: Path | None = None,
    cors_origins: list[str] | None = None,
) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        dashboard_path: Path to web dashboard static files (optional)
        cors_origins: List of allowed CORS origins (default: allow all)

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=APP_NAME,
        description="REST API for Obsidian-Supernote synchronization",
        version=API_VERSION,
        lifespan=lifespan,
    )

    # Configure CORS
    if cors_origins is None:
        cors_origins = ["*"]  # Allow all origins by default for local dev

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(status.router, tags=["Status"])
    app.include_router(convert.router, prefix="/convert", tags=["Conversion"])
    app.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])

    # WebSocket endpoint for real-time events
    @app.websocket("/events")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        """
        WebSocket endpoint for real-time progress updates.

        Connect to ws://host:port/events to receive:
        - Conversion progress events
        - Batch operation progress
        - Workflow execution updates
        """
        await ws_manager.connect(websocket)
        try:
            while True:
                # Keep connection alive and handle any client messages
                data = await websocket.receive_text()
                # Echo back or handle client messages if needed
                logger.debug(f"Received WebSocket message: {data}")
        except WebSocketDisconnect:
            ws_manager.disconnect(websocket)
            logger.info("WebSocket client disconnected")

    # Serve web dashboard if path provided
    if dashboard_path and dashboard_path.exists():
        app.mount(
            "/dashboard",
            StaticFiles(directory=str(dashboard_path), html=True),
            name="dashboard",
        )
        logger.info(f"Serving dashboard from {dashboard_path}")

    return app


def run_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    dashboard_path: Path | None = None,
    reload: bool = False,
) -> None:
    """
    Run the FastAPI server using uvicorn.

    Args:
        host: Host to bind to (default: 127.0.0.1 for local only)
        port: Port to listen on (default: 8765)
        dashboard_path: Path to web dashboard static files
        reload: Enable auto-reload for development
    """
    import uvicorn

    # Create app with configuration
    app = create_app(dashboard_path=dashboard_path)

    logger.info(f"Starting server at http://{host}:{port}")
    logger.info(f"API docs available at http://{host}:{port}/docs")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
    )


# For running directly with: python -m obsidian_supernote.api.server
if __name__ == "__main__":
    run_server()
