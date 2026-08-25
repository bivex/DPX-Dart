import os
import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ....domain.pattern import PATTERN_CATALOG
from ....domain.detection import DetectionReport
from ....application.scan_service import ScanService
from ..parsers.dart_parser import RegexDartParser
from ..detectors.dart_detector import DartPatternDetector

app = typer.Typer(help="🎯 DPX-Dart: Architectural Pattern & Static Analysis Engine for Dart 3.x & Flutter")
console = Console()


@app.command()
def version():
    """Print DPX-Dart version and engine info."""
    console.print(
        Panel(
            "[bold cyan]🎯 DPX-Dart v0.1.0[/bold cyan]\n"
            "[white]Hexagonal DDD Static Analysis Engine for Dart 3.x & Flutter[/white]\n"
            "[dim]https://github.com/bivex/DPX-Dart[/dim]",
            title="Engine Info",
            border_style="cyan",
        )
    )


@app.command()
def catalog():
    """Display the 44 supported architectural patterns and hazard catalog."""
    table = Table(
        title="📚 DPX-Dart Supported Pattern Catalog (44 Rules)",
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Pattern Type", style="bold white")
    table.add_column("Category", style="green")
    table.add_column("Default Weight", justify="center", style="yellow")
    table.add_column("Description", style="dim")

    for p_type, meta in PATTERN_CATALOG.items():
        weight_str = f"{int(meta.default_weight * 100)}%"
        table.add_row(meta.pattern_type.value, meta.category.value, weight_str, meta.description)

    console.print(table)


@app.command()
def scan(
    paths: List[str] = typer.Argument(..., help="Path(s) to Dart source file(s) or directories"),
    html: Optional[str] = typer.Option(None, "--html", "-H", help="Path to export interactive HTML HUD report"),
    json_path: Optional[str] = typer.Option(None, "--json", "-J", help="Path to export findings JSON report"),
    markdown: Optional[str] = typer.Option(None, "--markdown", "-M", help="Path to export findings Markdown report"),
    sarif: Optional[str] = typer.Option(None, "--sarif", "-S", help="Path to export SARIF v2.1.0 report"),
):
    """Scan Dart & Flutter codebases for architectural patterns and security hazards."""
    parser = RegexDartParser()
    detector = DartPatternDetector()
    service = ScanService(parser=parser, detector=detector)

    with console.status("[bold cyan]Scanning Dart/Flutter codebase for architectural patterns...[/bold cyan]"):
        report = service.scan_paths(
            paths=paths,
            html_out=html,
            json_out=json_path,
            md_out=markdown,
            sarif_out=sarif,
        )

    # Render summary table
    table = Table(
        title=f"🎯 DPX-Dart Findings Summary ({report.total_detections} detected in {report.execution_time_seconds:.4f}s)",
        header_style="bold cyan",
        border_style="cyan",
    )
    table.add_column("#", justify="center", style="dim")
    table.add_column("Category", style="green")
    table.add_column("Pattern Type", style="bold white")
    table.add_column("Target Symbol", style="cyan")
    table.add_column("Confidence", justify="center", style="yellow")
    table.add_column("Location", style="dim")

    for idx, d in enumerate(report.detections, start=1):
        loc_str = f"{os.path.basename(d.location.file_path)}:{d.location.line_number}"
        conf_str = f"{d.confidence.percentage}%\n[{d.confidence.level.value}]"
        table.add_row(
            str(idx),
            d.category.value,
            d.pattern_type.value,
            d.target_name,
            conf_str,
            loc_str,
        )

    console.print(table)

    if html:
        console.print(f"[bold green]✔[/bold green] Interactive HTML HUD exported to: [cyan]{html}[/cyan]")
    if json_path:
        console.print(f"[bold green]✔[/bold green] JSON findings exported to: [cyan]{json_path}[/cyan]")
    if markdown:
        console.print(f"[bold green]✔[/bold green] Markdown report exported to: [cyan]{markdown}[/cyan]")
    if sarif:
        console.print(f"[bold green]✔[/bold green] SARIF file exported to: [cyan]{sarif}[/cyan]")


if __name__ == "__main__":
    app()
