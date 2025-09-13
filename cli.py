# Purpose
# - Accept invoice JSON file as input
# - Trigger processing and rendering
# - Output paths to generated files

import typer
import json
from pathlib import Path
from app.services.invoice_processor import process_invoice
from app.services.smart_invoice_builder import build_invoice_from_items

app = typer.Typer()

def quick_generate(
    org_id: str = typer.Argument(..., help="Organization ID (matches config folder)"),
    items_file: str = typer.Argument(..., help="Path to JSON file with item descriptions"),
    output_dir: str = typer.Option("output", help="Directory to save generated invoice files")
):
    """
    Generate a full invoice from minimal input (just item descriptions).
    Auto-fills supplier, customer, HSN, tax rate, etc. from config.
    """
    try:
        with open(items_file, "r") as f:
            items_input = json.load(f)["items"]

        invoice_data = build_invoice_from_items(org_id, items_input)

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        result = process_invoice(invoice_data, output_dir)

        typer.echo("✅ Invoice generated successfully:")
        for fmt, path in result.items():
            typer.echo(f"  {fmt.upper()}: {path}")

    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)

app.command()(quick_generate)

if __name__ == "__main__":
    app()
