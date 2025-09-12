# Purpose
# - Accept invoice data via POST
# - Validate and process invoice
# - Return paths to generated files or raw tax breakdown
# - Handle errors gracefully

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.invoice_processor import process_invoice
import os

app = FastAPI(title="Invoice Generator API ")

class InvoiceInput(BaseModel):
    invoice: dict
    
@app.post("/generate")
def generate_invoice(payload: InvoiceInput):
    try:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        result = process_invoice(payload.invoice, output_dir)
        return {
            "message": "Invoice Processed Successfully", "files": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))