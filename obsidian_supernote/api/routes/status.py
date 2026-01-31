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

from fastapi import APIRouter, HTTPException
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


class FileInfo(BaseModel):
    """Information about a file or directory."""

    name: str
    path: str
    is_dir: bool
    size: int | None = None
    extension: str | None = None


class BrowseResponse(BaseModel):
    """Response for file browsing."""

    current_path: str
    parent_path: str | None
    items: list[FileInfo]


@router.get("/browse", response_model=BrowseResponse)
async def browse_files(
    path: str | None = None,
    filter_ext: str | None = None,
) -> BrowseResponse:
    """
    Browse files and directories on the local filesystem.

    Args:
        path: Directory path to browse (defaults to user home)
        filter_ext: Optional file extension filter (e.g., ".md", ".note")

    Returns:
        List of files and directories in the specified path
    """
    from pathlib import Path
    import os

    # Default to user home directory
    if not path:
        path = str(Path.home())

    browse_path = Path(path)

    if not browse_path.exists():
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")

    if not browse_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Not a directory: {path}")

    items: list[FileInfo] = []

    try:
        for entry in sorted(browse_path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower())):
            # Skip hidden files
            if entry.name.startswith('.'):
                continue

            is_dir = entry.is_dir()
            ext = entry.suffix.lower() if not is_dir else None

            # Apply extension filter for files
            if filter_ext and not is_dir:
                if ext != filter_ext.lower():
                    continue

            try:
                size = entry.stat().st_size if not is_dir else None
            except OSError:
                size = None

            items.append(FileInfo(
                name=entry.name,
                path=str(entry),
                is_dir=is_dir,
                size=size,
                extension=ext,
            ))
    except PermissionError:
        raise HTTPException(status_code=403, detail=f"Permission denied: {path}")

    # Get parent path
    parent = browse_path.parent
    parent_path = str(parent) if parent != browse_path else None

    return BrowseResponse(
        current_path=str(browse_path),
        parent_path=parent_path,
        items=items,
    )


@router.get("/drives")
async def list_drives() -> list[dict[str, str]]:
    """
    List available drives (Windows) or mount points (Unix).

    Returns:
        List of drive/mount point information
    """
    import platform
    from pathlib import Path

    drives = []

    if platform.system() == "Windows":
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if Path(drive).exists():
                drives.append({"path": drive, "name": f"{letter}:"})
    else:
        # Unix - show common mount points
        for mount in ["/", "/home", "/Users"]:
            if Path(mount).exists():
                drives.append({"path": mount, "name": mount})

    return drives


class FileDialogRequest(BaseModel):
    """Request for native file dialog."""

    mode: str = "file"  # "file" or "directory"
    title: str | None = None
    initial_dir: str | None = None
    file_types: list[tuple[str, str]] | None = None  # e.g., [("Markdown", "*.md")]


class FileDialogResponse(BaseModel):
    """Response from native file dialog."""

    selected: bool
    path: str | None = None


@router.post("/file-dialog", response_model=FileDialogResponse)
async def open_file_dialog(request: FileDialogRequest) -> FileDialogResponse:
    """
    Open native OS file/directory selection dialog.

    Args:
        request: Dialog configuration (mode, title, initial_dir, file_types)

    Returns:
        Selected file/directory path or None if cancelled
    """
    import threading
    from pathlib import Path

    result: dict[str, str | None] = {"path": None}

    def show_dialog() -> None:
        import tkinter as tk
        from tkinter import filedialog

        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # Bring dialog to front

        initial = request.initial_dir or str(Path.home())

        if request.mode == "directory":
            path = filedialog.askdirectory(
                title=request.title or "Select Directory",
                initialdir=initial,
            )
        else:
            # File selection
            filetypes = []
            if request.file_types:
                filetypes = [(name, pattern) for name, pattern in request.file_types]
            filetypes.append(("All files", "*.*"))

            path = filedialog.askopenfilename(
                title=request.title or "Select File",
                initialdir=initial,
                filetypes=filetypes,
            )

        result["path"] = path if path else None
        root.destroy()

    # Run dialog in separate thread to avoid blocking async event loop
    thread = threading.Thread(target=show_dialog)
    thread.start()
    thread.join(timeout=300)  # 5 minute timeout

    return FileDialogResponse(
        selected=result["path"] is not None,
        path=result["path"],
    )
