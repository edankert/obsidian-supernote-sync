"""
API route modules for Obsidian-Supernote Sync.

Each module provides endpoints for a specific domain:
- status: Health checks and version info
- convert: File conversion operations
- workflows: Workflow management and execution
"""

from obsidian_supernote.api.routes import convert, status, workflows

__all__ = ["convert", "status", "workflows"]
