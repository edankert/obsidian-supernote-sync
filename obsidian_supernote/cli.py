"""Command-line interface for Obsidian-Supernote Sync."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from obsidian_supernote import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="obsidian-supernote")
def main() -> None:
    """Obsidian-Supernote Sync Tool.

    Bi-directional synchronization between Obsidian vault and Supernote device.
    """
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--page-size", default="A4", help="PDF page size (A4, A5, Letter)")
@click.option("--dpi", default=300, help="Image DPI for quality")
def md_to_pdf(input_file: str, output_file: str, page_size: str, dpi: int) -> None:
    """Convert Markdown file to PDF for Supernote.

    Arguments:
        INPUT_FILE: Path to markdown file
        OUTPUT_FILE: Path to output PDF file
    """
    console.print(f"[bold green]Converting[/bold green] {input_file} -> {output_file}")
    console.print(f"Page size: {page_size}, DPI: {dpi}")

    # TODO: Implement conversion
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--ocr/--no-ocr", default=True, help="Enable OCR text extraction")
@click.option("--images/--no-images", default=True, help="Extract page images")
def note_to_md(input_file: str, output_file: str, ocr: bool, images: bool) -> None:
    """Convert Supernote .note file to Markdown.

    Arguments:
        INPUT_FILE: Path to .note file
        OUTPUT_FILE: Path to output markdown file
    """
    console.print(f"[bold green]Converting[/bold green] {input_file} -> {output_file}")
    console.print(f"OCR: {ocr}, Extract images: {images}")

    # TODO: Implement conversion
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


@main.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
@click.option("--dry-run", is_flag=True, help="Show what would be synced without doing it")
def sync(config: str | None, dry_run: bool) -> None:
    """Synchronize files between Obsidian and Supernote.

    This command performs bi-directional sync based on configuration.
    """
    console.print("[bold blue]Starting sync...[/bold blue]")

    if dry_run:
        console.print("[yellow]DRY RUN MODE - No files will be modified[/yellow]")

    # TODO: Implement sync
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


@main.command()
def status() -> None:
    """Show sync status and statistics."""
    console.print("[bold blue]Sync Status[/bold blue]\n")

    # TODO: Load actual status from database
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status")
    table.add_column("Count")

    table.add_row("Synced files", "0")
    table.add_row("Pending sync", "0")
    table.add_row("Conflicts", "0")
    table.add_row("Last sync", "Never")

    console.print(table)
    console.print("\n[yellow]Not yet implemented - Coming soon![/yellow]")


@main.command()
@click.argument("note_file", type=click.Path(exists=True))
def inspect(note_file: str) -> None:
    """Inspect a Supernote .note file structure.

    Arguments:
        NOTE_FILE: Path to .note file to inspect
    """
    console.print(f"[bold blue]Inspecting[/bold blue] {note_file}\n")

    # TODO: Implement inspection using note parser
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


@main.command()
def init() -> None:
    """Initialize configuration and setup sync directories."""
    console.print("[bold blue]Initializing Obsidian-Supernote Sync[/bold blue]\n")

    # TODO: Create config file, sync directories, database
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


if __name__ == "__main__":
    main()
