"""
Conversion endpoints for Obsidian-Supernote Sync.

Provides:
- /convert/md-to-note - Convert Markdown to .note
- /convert/note-to-md - Convert .note to Markdown
- /convert/pdf-to-note - Convert PDF to .note
- /convert/png-to-note - Convert PNG to .note
- /batch/convert - Batch conversion operations
"""

import asyncio
import logging
import os
import tempfile
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from obsidian_supernote.api.websocket import (
    ProgressReporter,
    BatchProgressReporter,
    manager as ws_manager,
)

logger = logging.getLogger(__name__)
router = APIRouter()


# Request/Response Models

class MarkdownToNoteRequest(BaseModel):
    """Request to convert Markdown to .note file."""

    input_path: str = Field(..., description="Path to input Markdown file")
    output_path: str = Field(..., description="Path for output .note file")
    device: str = Field(default="A5X2", description="Target device (A5X, A5X2, A6X, A6X2)")
    realtime: bool | None = Field(
        default=None,
        description="Enable realtime recognition. If None, reads from frontmatter"
    )
    page_size: str = Field(default="A5", description="PDF page size (A4, A5, A6, Letter)")
    margin: str = Field(default="2cm", description="Page margins")
    font_size: int = Field(default=11, description="Base font size in points")
    update_markdown: bool = Field(
        default=True,
        description="Update markdown frontmatter with .note file reference"
    )


class NoteToMarkdownRequest(BaseModel):
    """Request to convert .note file to Markdown."""

    input_path: str = Field(..., description="Path to input .note file")
    output_path: str = Field(..., description="Path for output Markdown file")
    image_dir: str | None = Field(
        default=None,
        description="Directory for extracted images (default: same as output)"
    )


class PdfToNoteRequest(BaseModel):
    """Request to convert PDF to .note file."""

    input_path: str = Field(..., description="Path to input PDF file")
    output_path: str = Field(..., description="Path for output .note file")
    device: str = Field(default="A5X2", description="Target device")
    realtime: bool = Field(default=False, description="Enable realtime recognition")


class PngToNoteRequest(BaseModel):
    """Request to convert PNG to .note file."""

    input_path: str = Field(..., description="Path to input PNG file")
    output_path: str = Field(..., description="Path for output .note file")
    device: str = Field(default="A5X2", description="Target device")
    template_name: str | None = Field(default=None, description="Template name")
    realtime: bool = Field(default=False, description="Enable realtime recognition")


class BatchConvertRequest(BaseModel):
    """Request to batch convert multiple files."""

    conversion_type: Literal["md-to-note", "note-to-md", "pdf-to-note", "png-to-note"]
    input_paths: list[str] = Field(..., description="List of input file paths")
    output_dir: str = Field(..., description="Output directory for converted files")
    device: str = Field(default="A5X2", description="Target device (for *-to-note)")
    realtime: bool = Field(default=False, description="Enable realtime recognition")


class ConversionResult(BaseModel):
    """Result of a conversion operation."""

    success: bool
    input_path: str
    output_path: str | None = None
    error: str | None = None
    message: str | None = None


class BatchConversionResult(BaseModel):
    """Result of a batch conversion operation."""

    total: int
    successful: int
    failed: int
    results: list[ConversionResult]


# Helper functions

def _validate_file_exists(path: str, file_type: str = "file") -> Path:
    """Validate that a file exists and return Path object."""
    p = Path(path)
    if not p.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Input {file_type} not found: {path}"
        )
    return p


def _ensure_output_dir(path: str) -> Path:
    """Ensure output directory exists."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


# Endpoints

@router.post("/md-to-note", response_model=ConversionResult)
async def convert_markdown_to_note(request: MarkdownToNoteRequest) -> ConversionResult:
    """
    Convert a Markdown file to Supernote .note format.

    This wraps the existing converter and:
    - Reads frontmatter properties (supernote.type, supernote.file)
    - Optionally updates markdown with .note file reference
    - Supports update mode (preserving handwriting in existing .note)
    - Broadcasts WebSocket progress events
    """
    reporter = ProgressReporter("md-to-note", request.input_path)

    try:
        from obsidian_supernote.converters import convert_markdown_to_note as _convert

        input_path = _validate_file_exists(request.input_path, "Markdown file")
        output_path = _ensure_output_dir(request.output_path)

        # Broadcast start event
        await reporter.start()
        await reporter.progress(0.1, "Reading markdown file...")

        # Run conversion in thread pool to not block event loop
        await reporter.progress(0.3, "Converting to PDF...")

        def do_conversion() -> None:
            _convert(
                markdown_path=input_path,
                output_path=output_path,
                device=request.device,
                realtime=request.realtime,
                page_size=request.page_size,
                margin=request.margin,
                font_size=request.font_size,
                update_markdown=request.update_markdown,
            )

        await asyncio.get_event_loop().run_in_executor(None, do_conversion)

        await reporter.progress(0.9, "Finalizing...")
        await reporter.complete(str(output_path))

        return ConversionResult(
            success=True,
            input_path=str(input_path),
            output_path=str(output_path),
            message=f"Successfully converted to {output_path}",
        )

    except HTTPException:
        raise
    except FileNotFoundError as e:
        await reporter.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to convert {request.input_path}")
        await reporter.error(str(e))
        return ConversionResult(
            success=False,
            input_path=request.input_path,
            error=str(e),
        )


@router.post("/note-to-md", response_model=ConversionResult)
async def convert_note_to_markdown(request: NoteToMarkdownRequest) -> ConversionResult:
    """
    Convert a Supernote .note file to Markdown with embedded images.

    Extracts all pages as PNG images and creates a Markdown file
    with Obsidian-compatible image embeds. Broadcasts WebSocket progress events.
    """
    reporter = ProgressReporter("note-to-md", request.input_path)

    try:
        from obsidian_supernote.converters import convert_note_to_markdown as _convert

        input_path = _validate_file_exists(request.input_path, ".note file")
        output_path = _ensure_output_dir(request.output_path)

        image_dir = Path(request.image_dir) if request.image_dir else None

        await reporter.start()
        await reporter.progress(0.2, "Reading .note file...")

        def do_conversion() -> Path:
            return _convert(
                note_path=input_path,
                output_path=output_path,
                image_dir=image_dir,
            )

        await reporter.progress(0.5, "Extracting pages...")
        result_path = await asyncio.get_event_loop().run_in_executor(None, do_conversion)

        await reporter.progress(0.9, "Creating markdown...")
        await reporter.complete(str(result_path))

        return ConversionResult(
            success=True,
            input_path=str(input_path),
            output_path=str(result_path),
            message=f"Successfully exported to {result_path}",
        )

    except HTTPException:
        raise
    except FileNotFoundError as e:
        await reporter.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to convert {request.input_path}")
        await reporter.error(str(e))
        return ConversionResult(
            success=False,
            input_path=request.input_path,
            error=str(e),
        )


@router.post("/pdf-to-note", response_model=ConversionResult)
async def convert_pdf_to_note(request: PdfToNoteRequest) -> ConversionResult:
    """
    Convert a PDF file to Supernote .note format.

    The PDF pages become the background template that can be
    annotated on the Supernote device. Broadcasts WebSocket progress events.
    """
    reporter = ProgressReporter("pdf-to-note", request.input_path)

    try:
        from obsidian_supernote.converters import convert_pdf_to_note as _convert

        input_path = _validate_file_exists(request.input_path, "PDF file")
        output_path = _ensure_output_dir(request.output_path)

        await reporter.start()
        await reporter.progress(0.2, "Reading PDF file...")

        def do_conversion() -> None:
            _convert(
                pdf_path=input_path,
                output_path=output_path,
                device=request.device,
                realtime=request.realtime,
            )

        await reporter.progress(0.5, "Converting pages to .note format...")
        await asyncio.get_event_loop().run_in_executor(None, do_conversion)

        await reporter.complete(str(output_path))

        return ConversionResult(
            success=True,
            input_path=str(input_path),
            output_path=str(output_path),
            message=f"Successfully converted to {output_path}",
        )

    except HTTPException:
        raise
    except FileNotFoundError as e:
        await reporter.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to convert {request.input_path}")
        await reporter.error(str(e))
        return ConversionResult(
            success=False,
            input_path=request.input_path,
            error=str(e),
        )


@router.post("/png-to-note", response_model=ConversionResult)
async def convert_png_to_note(request: PngToNoteRequest) -> ConversionResult:
    """
    Convert a PNG template to Supernote .note format.

    Creates a .note file with the PNG as the background template.
    Broadcasts WebSocket progress events.
    """
    reporter = ProgressReporter("png-to-note", request.input_path)

    try:
        from obsidian_supernote.converters import convert_png_to_note as _convert

        input_path = _validate_file_exists(request.input_path, "PNG file")
        output_path = _ensure_output_dir(request.output_path)

        await reporter.start()
        await reporter.progress(0.3, "Reading PNG template...")

        def do_conversion() -> None:
            _convert(
                png_path=input_path,
                output_path=output_path,
                device=request.device,
                template_name=request.template_name,
                realtime=request.realtime,
            )

        await reporter.progress(0.6, "Creating .note file...")
        await asyncio.get_event_loop().run_in_executor(None, do_conversion)

        await reporter.complete(str(output_path))

        return ConversionResult(
            success=True,
            input_path=str(input_path),
            output_path=str(output_path),
            message=f"Successfully converted to {output_path}",
        )

    except HTTPException:
        raise
    except FileNotFoundError as e:
        await reporter.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to convert {request.input_path}")
        await reporter.error(str(e))
        return ConversionResult(
            success=False,
            input_path=request.input_path,
            error=str(e),
        )


@router.post("/batch", response_model=BatchConversionResult)
async def batch_convert(request: BatchConvertRequest) -> BatchConversionResult:
    """
    Batch convert multiple files.

    Supports:
    - md-to-note: Markdown files to .note
    - note-to-md: .note files to Markdown
    - pdf-to-note: PDF files to .note
    - png-to-note: PNG files to .note

    Broadcasts WebSocket progress events for each file.
    """
    results: list[ConversionResult] = []
    output_dir = Path(request.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Map conversion type to the appropriate converter function
    converters = {
        "md-to-note": _batch_md_to_note,
        "note-to-md": _batch_note_to_md,
        "pdf-to-note": _batch_pdf_to_note,
        "png-to-note": _batch_png_to_note,
    }

    converter_func = converters.get(request.conversion_type)
    if not converter_func:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown conversion type: {request.conversion_type}"
        )

    # Create batch progress reporter
    batch_reporter = BatchProgressReporter(len(request.input_paths))
    await batch_reporter.start()

    for i, input_path in enumerate(request.input_paths):
        await batch_reporter.file_progress(i, input_path, "converting")

        result = await converter_func(
            input_path=input_path,
            output_dir=output_dir,
            device=request.device,
            realtime=request.realtime,
        )
        results.append(result)

        await batch_reporter.file_complete(
            i,
            input_path,
            result.output_path,
            result.error,
        )

    await batch_reporter.complete()

    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful

    return BatchConversionResult(
        total=len(results),
        successful=successful,
        failed=failed,
        results=results,
    )


# Batch helper functions

async def _batch_md_to_note(
    input_path: str,
    output_dir: Path,
    device: str,
    realtime: bool,
) -> ConversionResult:
    """Batch convert a single Markdown file."""
    try:
        from obsidian_supernote.converters import convert_markdown_to_note as _convert

        p = Path(input_path)
        if not p.exists():
            return ConversionResult(
                success=False,
                input_path=input_path,
                error=f"File not found: {input_path}",
            )

        output_path = output_dir / f"{p.stem}.note"
        _convert(
            markdown_path=p,
            output_path=output_path,
            device=device,
            realtime=realtime,
        )

        return ConversionResult(
            success=True,
            input_path=input_path,
            output_path=str(output_path),
        )
    except Exception as e:
        return ConversionResult(
            success=False,
            input_path=input_path,
            error=str(e),
        )


async def _batch_note_to_md(
    input_path: str,
    output_dir: Path,
    device: str,
    realtime: bool,
) -> ConversionResult:
    """Batch convert a single .note file."""
    try:
        from obsidian_supernote.converters import convert_note_to_markdown as _convert

        p = Path(input_path)
        if not p.exists():
            return ConversionResult(
                success=False,
                input_path=input_path,
                error=f"File not found: {input_path}",
            )

        output_path = output_dir / f"{p.stem}.md"
        _convert(
            note_path=p,
            output_path=output_path,
        )

        return ConversionResult(
            success=True,
            input_path=input_path,
            output_path=str(output_path),
        )
    except Exception as e:
        return ConversionResult(
            success=False,
            input_path=input_path,
            error=str(e),
        )


async def _batch_pdf_to_note(
    input_path: str,
    output_dir: Path,
    device: str,
    realtime: bool,
) -> ConversionResult:
    """Batch convert a single PDF file."""
    try:
        from obsidian_supernote.converters import convert_pdf_to_note as _convert

        p = Path(input_path)
        if not p.exists():
            return ConversionResult(
                success=False,
                input_path=input_path,
                error=f"File not found: {input_path}",
            )

        output_path = output_dir / f"{p.stem}.note"
        _convert(
            pdf_path=p,
            output_path=output_path,
            device=device,
            realtime=realtime,
        )

        return ConversionResult(
            success=True,
            input_path=input_path,
            output_path=str(output_path),
        )
    except Exception as e:
        return ConversionResult(
            success=False,
            input_path=input_path,
            error=str(e),
        )


async def _batch_png_to_note(
    input_path: str,
    output_dir: Path,
    device: str,
    realtime: bool,
) -> ConversionResult:
    """Batch convert a single PNG file."""
    try:
        from obsidian_supernote.converters import convert_png_to_note as _convert

        p = Path(input_path)
        if not p.exists():
            return ConversionResult(
                success=False,
                input_path=input_path,
                error=f"File not found: {input_path}",
            )

        output_path = output_dir / f"{p.stem}.note"
        _convert(
            png_path=p,
            output_path=output_path,
            device=device,
            realtime=realtime,
        )

        return ConversionResult(
            success=True,
            input_path=input_path,
            output_path=str(output_path),
        )
    except Exception as e:
        return ConversionResult(
            success=False,
            input_path=input_path,
            error=str(e),
        )
