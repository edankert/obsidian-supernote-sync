"""Command-line interface for Obsidian-Supernote Sync."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint

from obsidian_supernote import __version__
from obsidian_supernote.converters.pandoc_converter import PandocConverter
from obsidian_supernote.converters import WEASYPRINT_AVAILABLE
from obsidian_supernote.parsers.note_parser import NoteFileParser

# Conditionally import WeasyPrint converter
if WEASYPRINT_AVAILABLE:
    from obsidian_supernote.converters.markdown_to_pdf import MarkdownToPdfConverter

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
@click.option("--page-size", default="A5", help="PDF page size (A4, A5, A6, Letter)")
@click.option("--margin", default="2cm", help="Page margins (e.g., 2cm, 1in)")
@click.option("--font-size", default=11, help="Base font size in points")
@click.option("--engine", type=click.Choice(["pandoc", "weasyprint"], case_sensitive=False), default="pandoc", help="PDF conversion engine")
@click.option("--css", type=click.Path(exists=True), help="Custom CSS file for styling")
def md_to_pdf(
    input_file: str,
    output_file: str,
    page_size: str,
    margin: str,
    font_size: int,
    engine: str,
    css: str | None,
) -> None:
    """Convert Markdown file to PDF for Supernote.

    By default uses Pandoc (recommended - easier to install).
    Can also use WeasyPrint with --engine weasyprint (requires GTK+).

    Arguments:
        INPUT_FILE: Path to markdown file
        OUTPUT_FILE: Path to output PDF file
    """
    try:
        input_path = Path(input_file)
        output_path = Path(output_file)
        css_path = Path(css) if css else None

        console.print(f"[bold blue]Converting Markdown → PDF[/bold blue]")
        console.print(f"  Input:    {input_path}")
        console.print(f"  Output:   {output_path}")
        console.print(f"  Page:     {page_size}")
        console.print(f"  Margin:   {margin}")
        console.print(f"  Font:     {font_size}pt")
        console.print(f"  Engine:   {engine}")

        # Choose conversion engine
        if engine == "pandoc":
            converter = PandocConverter(
                page_size=page_size,
                margin=margin,
                font_size=font_size,
            )
            with console.status("[bold green]Converting with Pandoc...", spinner="dots"):
                converter.convert(input_path, output_path, css_file=css_path)

        elif engine == "weasyprint":
            if not WEASYPRINT_AVAILABLE:
                console.print("[bold red]✗ Error:[/bold red] WeasyPrint is not available.")
                console.print("  WeasyPrint requires GTK+ libraries on Windows.")
                console.print("  See docs/WEASYPRINT_SETUP.md for installation.")
                console.print("\n  [cyan]Tip:[/cyan] Use --engine pandoc instead (default)")
                raise click.Abort()

            # Use DPI for WeasyPrint (Pandoc doesn't use DPI)
            converter = MarkdownToPdfConverter(page_size=page_size, dpi=300)
            with console.status("[bold green]Converting with WeasyPrint...", spinner="dots"):
                converter.convert(input_path, output_path, css_path)

        # Get file size
        size_kb = output_path.stat().st_size / 1024

        console.print(f"\n[bold green]SUCCESS![/bold green]")
        console.print(f"  Generated: {output_path}")
        console.print(f"  Size: {size_kb:.1f} KB")

    except RuntimeError as e:
        console.print(f"[bold red]ERROR:[/bold red] {e}")
        if "Pandoc is not installed" in str(e):
            console.print("\n[cyan]Installation:[/cyan]")
            console.print("  Windows: choco install pandoc")
            console.print("  Mac:     brew install pandoc")
            console.print("  Linux:   apt install pandoc")
            console.print("  Or:      https://pandoc.org/installing.html")
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {e}")
        raise click.Abort()


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
@click.option("--save-images", type=click.Path(), help="Directory to save extracted PNG images")
def inspect(note_file: str, save_images: str | None) -> None:
    """Inspect a Supernote .note file structure.

    Arguments:
        NOTE_FILE: Path to .note file to inspect
    """
    try:
        note_path = Path(note_file)

        console.print(Panel.fit(
            f"[bold cyan]Inspecting Supernote .note File[/bold cyan]\n{note_path}",
            border_style="cyan"
        ))

        # Parse the file
        with console.status("[bold green]Parsing file...", spinner="dots"):
            parser = NoteFileParser(note_path)
            data = parser.parse()
            summary = parser.get_summary()

        # Display summary
        console.print("\n[bold]File Summary:[/bold]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("File name", summary["file_name"])
        table.add_row("File size", f"{summary['file_size_mb']} MB")
        table.add_row("Format version", summary["format_version"])
        table.add_row("File type", summary["file_type"])
        table.add_row("Device", summary["device"])
        table.add_row("Language", summary["language"])
        table.add_row("PDF template", summary["pdf_template"])
        table.add_row("Template MD5", summary["pdf_template_md5"][:32] + "..." if len(summary["pdf_template_md5"]) > 32 else summary["pdf_template_md5"])

        console.print(table)

        # Display PNG information
        console.print(f"\n[bold]Embedded Images:[/bold]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("PNG count", str(summary["png_images_count"]))
        table.add_row("Images size", f"{summary['png_images_size_mb']} MB")

        if summary["png_images_count"] > 0:
            # Get dimensions of first image
            first_img = parser.get_png_image(0)
            if first_img:
                table.add_row("Dimensions", f"{first_img.width} x {first_img.height} pixels")
                table.add_row("Mode", first_img.mode)

        console.print(table)

        # Display ZIP archive information
        console.print(f"\n[bold]Handwriting Data (ZIP):[/bold]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Archive size", f"{summary['zip_archive_size_kb']} KB")
        table.add_row("Pages", str(summary["pages_count"]))
        table.add_row("Has handwriting", "Yes" if summary["has_handwriting"] else "No")

        # Show ZIP metadata if available
        if "meta" in data["zip_contents"]:
            meta = data["zip_contents"]["meta"]
            table.add_row("Application", meta.get("Application", "Unknown"))
            table.add_row("App version", meta.get("Application_Version", "Unknown"))
            table.add_row("Format version", meta.get("format-version", "Unknown"))

        console.print(table)

        # Display page details
        if data["zip_contents"].get("pages"):
            console.print(f"\n[bold]Pages Detail:[/bold]")
            pages_table = Table(show_header=True, box=None)
            pages_table.add_column("Page ID", style="cyan")
            pages_table.add_column("Has Content", style="white")
            pages_table.add_column("Ink Size", style="white", justify="right")

            for page_id, page_data in data["zip_contents"]["pages"].items():
                has_content = "Yes" if page_data.get("has_content") else "No"
                ink_size = f"{page_data.get('ink_size', 0) / 1024:.1f} KB" if page_data.get("ink_size") else "N/A"
                pages_table.add_row(page_id, has_content, ink_size)

            console.print(pages_table)

        # Save images if requested
        if save_images and summary["png_images_count"] > 0:
            output_dir = Path(save_images)
            console.print(f"\n[bold]Saving images to {output_dir}...[/bold]")
            saved_files = parser.save_png_images(output_dir)
            for f in saved_files:
                console.print(f"  [green]OK[/green] {f.name}")

        console.print(f"\n[bold green]SUCCESS: Inspection complete![/bold green]")

    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {e}")
        import traceback
        console.print(traceback.format_exc())
        raise click.Abort()


@main.command()
def init() -> None:
    """Initialize configuration and setup sync directories."""
    console.print("[bold blue]Initializing Obsidian-Supernote Sync[/bold blue]\n")

    # TODO: Create config file, sync directories, database
    console.print("[yellow]Not yet implemented - Coming soon![/yellow]")


if __name__ == "__main__":
    main()
