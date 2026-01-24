"""
WebSocket support for real-time progress updates.

This module provides:
- ConnectionManager: Manages WebSocket connections
- Progress events: Broadcast conversion progress to connected clients
- Event types: conversion_started, conversion_progress, conversion_complete, conversion_error
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of WebSocket events."""

    # Connection events
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"

    # Conversion events
    CONVERSION_STARTED = "conversion_started"
    CONVERSION_PROGRESS = "conversion_progress"
    CONVERSION_COMPLETE = "conversion_complete"
    CONVERSION_ERROR = "conversion_error"

    # Batch events
    BATCH_STARTED = "batch_started"
    BATCH_PROGRESS = "batch_progress"
    BATCH_COMPLETE = "batch_complete"

    # Workflow events
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_STEP = "workflow_step"
    WORKFLOW_COMPLETE = "workflow_complete"
    WORKFLOW_ERROR = "workflow_error"


@dataclass
class ProgressEvent:
    """A progress event to broadcast to clients."""

    event_type: EventType
    task_id: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_json(self) -> str:
        """Convert to JSON string for WebSocket transmission."""
        return json.dumps({
            "type": event_type_to_str(self.event_type),
            "task_id": self.task_id,
            "data": self.data,
            "timestamp": self.timestamp,
        })


def event_type_to_str(event_type: EventType) -> str:
    """Convert EventType to string value."""
    return event_type.value


class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts events.

    Usage:
        manager = ConnectionManager()

        # In WebSocket endpoint
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)

        # Broadcast events
        await manager.broadcast_event(ProgressEvent(...))
    """

    def __init__(self) -> None:
        """Initialize connection manager."""
        self.active_connections: list[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

        # Send connected event
        await self.send_personal_event(
            websocket,
            ProgressEvent(
                event_type=EventType.CONNECTED,
                task_id="connection",
                data={"message": "Connected to Obsidian-Supernote API"},
            ),
        )

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_event(self, websocket: WebSocket, event: ProgressEvent) -> None:
        """Send an event to a specific connection."""
        try:
            await websocket.send_text(event.to_json())
        except Exception as e:
            logger.warning(f"Failed to send event to websocket: {e}")

    async def broadcast_event(self, event: ProgressEvent) -> None:
        """Broadcast an event to all connected clients."""
        if not self.active_connections:
            return

        message = event.to_json()
        disconnected: list[WebSocket] = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to broadcast to connection: {e}")
                disconnected.append(connection)

        # Clean up disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_json(self, data: dict[str, Any]) -> None:
        """Broadcast raw JSON data to all connected clients."""
        if not self.active_connections:
            return

        message = json.dumps(data)
        disconnected: list[WebSocket] = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    @property
    def connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()


class ProgressReporter:
    """
    Context manager for reporting conversion progress.

    Usage:
        async with ProgressReporter("conversion", input_path) as reporter:
            await reporter.progress(0.25, "Converting to PDF...")
            # ... do work ...
            await reporter.progress(0.75, "Creating .note file...")
            # ... do work ...
            await reporter.complete(output_path)
    """

    def __init__(
        self,
        task_type: str,
        input_path: str,
        manager: ConnectionManager = manager,
    ) -> None:
        """
        Initialize progress reporter.

        Args:
            task_type: Type of task (conversion, batch, workflow)
            input_path: Path to input file
            manager: ConnectionManager instance
        """
        self.task_id = str(uuid4())
        self.task_type = task_type
        self.input_path = input_path
        self.manager = manager
        self._started = False

    async def __aenter__(self) -> "ProgressReporter":
        """Start the task and send started event."""
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Handle task completion or error."""
        if exc_val is not None:
            await self.error(str(exc_val))
        # Note: complete() should be called explicitly with output path

    async def start(self) -> None:
        """Send task started event."""
        if self._started:
            return
        self._started = True

        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.CONVERSION_STARTED,
                task_id=self.task_id,
                data={
                    "task_type": self.task_type,
                    "input_path": self.input_path,
                },
            )
        )

    async def progress(self, percent: float, message: str = "") -> None:
        """
        Send progress update.

        Args:
            percent: Progress percentage (0.0 to 1.0)
            message: Optional status message
        """
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.CONVERSION_PROGRESS,
                task_id=self.task_id,
                data={
                    "percent": min(max(percent, 0.0), 1.0),
                    "message": message,
                    "input_path": self.input_path,
                },
            )
        )

    async def complete(self, output_path: str, message: str = "Conversion complete") -> None:
        """
        Send task complete event.

        Args:
            output_path: Path to output file
            message: Completion message
        """
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.CONVERSION_COMPLETE,
                task_id=self.task_id,
                data={
                    "input_path": self.input_path,
                    "output_path": output_path,
                    "message": message,
                },
            )
        )

    async def error(self, error_message: str) -> None:
        """
        Send task error event.

        Args:
            error_message: Error description
        """
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.CONVERSION_ERROR,
                task_id=self.task_id,
                data={
                    "input_path": self.input_path,
                    "error": error_message,
                },
            )
        )


class BatchProgressReporter:
    """
    Progress reporter for batch operations.

    Usage:
        reporter = BatchProgressReporter(file_count, manager)
        await reporter.start()
        for i, file in enumerate(files):
            await reporter.file_progress(i, file, "processing")
            # process file
            await reporter.file_complete(i, file, output_path)
        await reporter.complete()
    """

    def __init__(
        self,
        total_files: int,
        manager: ConnectionManager = manager,
    ) -> None:
        """Initialize batch progress reporter."""
        self.task_id = str(uuid4())
        self.total_files = total_files
        self.manager = manager
        self.completed = 0
        self.failed = 0

    async def start(self) -> None:
        """Send batch started event."""
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.BATCH_STARTED,
                task_id=self.task_id,
                data={
                    "total_files": self.total_files,
                },
            )
        )

    async def file_progress(self, index: int, file_path: str, status: str) -> None:
        """Send progress for current file."""
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.BATCH_PROGRESS,
                task_id=self.task_id,
                data={
                    "current_file": index + 1,
                    "total_files": self.total_files,
                    "file_path": file_path,
                    "status": status,
                    "percent": (index + 1) / self.total_files,
                },
            )
        )

    async def file_complete(self, index: int, input_path: str, output_path: str | None, error: str | None = None) -> None:
        """Mark a file as complete."""
        if error:
            self.failed += 1
        else:
            self.completed += 1

        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.BATCH_PROGRESS,
                task_id=self.task_id,
                data={
                    "current_file": index + 1,
                    "total_files": self.total_files,
                    "input_path": input_path,
                    "output_path": output_path,
                    "error": error,
                    "completed": self.completed,
                    "failed": self.failed,
                    "percent": (index + 1) / self.total_files,
                },
            )
        )

    async def complete(self) -> None:
        """Send batch complete event."""
        await self.manager.broadcast_event(
            ProgressEvent(
                event_type=EventType.BATCH_COMPLETE,
                task_id=self.task_id,
                data={
                    "total_files": self.total_files,
                    "completed": self.completed,
                    "failed": self.failed,
                },
            )
        )
