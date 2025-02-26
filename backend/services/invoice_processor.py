import pdfplumber
import json
import google.generativeai as genai
from pathlib import Path
from .inventory import update_inventory

def extract_text_from_pdf(pdf_path: Path) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    print("has been extracted")
    return text.strip()

def parse_invoice_with_gemini(invoice_text: str) -> dict:
    prompt = f"""
    Extract structured invoice details from the text below and return as JSON.
    
    Invoice Text:
    {invoice_text}

    Expected JSON format:
    {{
        "Invoice Number": "12345",
        "Supplier Info": {{
            "Name": "ABC Wholesale",
            "Address": "32nd Avenue, Gurgaon"
        }},
        "Date": "2025-02-24",
        "Items": [
            {{"name": "Sugar", "quantity": 10, "price": 50}}
        ],
        "Total": 655
    }}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        print("has been parsed")
        return json.loads(response.text.strip("```json").strip("\n```").strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse invoice"}

def process_invoice(pdf_path: Path) -> dict:
    invoice_text = extract_text_from_pdf(pdf_path)
    update_inventory(parse_invoice_with_gemini(invoice_text))
