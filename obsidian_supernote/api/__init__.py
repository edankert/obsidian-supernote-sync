"""
FastAPI backend for Obsidian-Supernote Sync.

This package provides a REST API server that wraps the existing
converter functionality, enabling integration with:
- Obsidian Plugin (TypeScript)
- Web Dashboard (React)
- Custom automation scripts

WebSocket Support:
- Connect to /events for real-time progress updates
- Conversion progress, batch progress, workflow events
"""

from obsidian_supernote.api.server import create_app, run_server
from obsidian_supernote.api.websocket import (
    ConnectionManager,
    ProgressReporter,
    BatchProgressReporter,
    EventType,
    ProgressEvent,
    manager as ws_manager,
)

__all__ = [
    "create_app",
    "run_server",
    "ConnectionManager",
    "ProgressReporter",
    "BatchProgressReporter",
    "EventType",
    "ProgressEvent",
    "ws_manager",
]
