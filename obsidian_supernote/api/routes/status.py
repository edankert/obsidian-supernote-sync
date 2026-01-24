"""
Status and health check endpoints.

Provides:
- /status - Overall system health and version info
- /status/dependencies - Check availability of external tools
"""

import shutil
import subprocess
from datetime import datetime
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DependencyStatus(BaseModel):
    """Status of an external dependency."""

    name: str
    available: bool
    version: str | None = None
    path: str | None = None


class SystemStatus(BaseModel):
    """Overall system status response."""

    status: str
    version: str
    timestamp: str
    uptime_seconds: float | None = None
    dependencies: dict[str, DependencyStatus] | None = None


# Track server start time
_start_time: datetime | None = None


def set_start_time() -> None:
    """Set the server start time (called on startup)."""
    global _start_time
    _start_time = datetime.now()


def _check_pandoc() -> DependencyStatus:
    """Check if Pandoc is available."""
    pandoc_path = shutil.which("pandoc")
    if pandoc_path:
        try:
            result = subprocess.run(
                ["pandoc", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            version_line = result.stdout.split("\n")[0] if result.stdout else None
            version = version_line.split()[-1] if version_line else None
            return DependencyStatus(
                name="pandoc",
                available=True,
                version=version,
                path=pandoc_path,
            )
        except Exception:
            pass
    return DependencyStatus(name="pandoc", available=False)


def _check_supernotelib() -> DependencyStatus:
    """Check if supernotelib is available."""
    try:
        import supernotelib

        version = getattr(supernotelib, "__version__", "unknown")
        return DependencyStatus(
            name="supernotelib",
            available=True,
            version=version,
        )
    except ImportError:
        return DependencyStatus(name="supernotelib", available=False)


def _check_pillow() -> DependencyStatus:
    """Check if Pillow is available."""
    try:
        from PIL import Image

        import PIL

        version = PIL.__version__
        return DependencyStatus(
            name="pillow",
            available=True,
            version=version,
        )
    except ImportError:
        return DependencyStatus(name="pillow", available=False)


@router.get("/status", response_model=SystemStatus)
async def get_status() -> SystemStatus:
    """
    Get system status and health information.

    Returns:
        SystemStatus with version, timestamp, and basic health info
    """
    from obsidian_supernote.api.server import API_VERSION

    uptime = None
    if _start_time:
        uptime = (datetime.now() - _start_time).total_seconds()

    return SystemStatus(
        status="healthy",
        version=API_VERSION,
        timestamp=datetime.now().isoformat(),
        uptime_seconds=uptime,
    )


@router.get("/status/dependencies", response_model=dict[str, DependencyStatus])
async def get_dependencies() -> dict[str, DependencyStatus]:
    """
    Check status of all external dependencies.

    Returns:
        Dictionary of dependency names to their status
    """
    return {
        "pandoc": _check_pandoc(),
        "supernotelib": _check_supernotelib(),
        "pillow": _check_pillow(),
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Simple health check endpoint for load balancers.

    Returns:
        {"status": "ok"}
    """
    return {"status": "ok"}
