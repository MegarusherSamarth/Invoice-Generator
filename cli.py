# Purpose
# - Accept invoice JSON file as input
# - Trigger processing and rendering
# - Output paths to generated files

import typer
import json
from pathlib import Path
from app.services.invoice_processor import process_invoice

app = typer.Typer()

@app.command()
def generate(
    input_file: str = typer.Argument(..., help="Path to invoice JSON file"),
    output_dir: str= typer.Option("output", help="Directory to save generated files")
):
    """Generate invoice PDF, JSON, and CSV from input JSON."""
    try:
        with open(input_file, "r") as f:
            invoice_data = json.load(f)
        
        Path(output_dir).mmkdir(parents=True, exist_ok= True)
        result = process_invoice(invoice_data, output_dir)
        
        typer.echo("Invoice Generated: ")
        for fwt, path in result.items():
            typer.echo(f" {fmt.upper()}: {path}")
    
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    app()