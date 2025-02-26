from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
import pdfplumber
import google.generativeai as genai
import json
import os
import pandas as pd
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
from services import gemini_service, invoice_processor, sales_forecast, analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3039"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    file_attached: bool = False 

@app.get("/")
def root():
    return {"message": "Supermarket Assistant API is running"}


@app.post("/chat")
async def chat_with_bot(
    message: str = Form(""),
    file: UploadFile = File(None),  
    user_id: str = Form(...)
):
    file_attached = file is not None

    if not message and not file:
        raise HTTPException(status_code=400, detail="Either message or file is required")

    # If a file is uploaded, save it temporarily
    file_path = None
    if file_attached:
        file_path = f"./uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("sending to invoice_processor")
        invoice_processor.process_invoice(file_path)

    # Send data to Gemini AI service
    response = gemini_service.analyze_input(message, file_attached, user_id, file_path)

    return {"response": response}



@app.get("/productdis")
def get_product_distribution(metric: str = "Total"):
    return analysis.product_distribution(metric)

@app.get("/gross-income")
async def get_gross_income():
    return analysis.gross_income()

@app.get("/total-sales")
async def get_gross_income():
    return analysis.total_sales()

@app.get("/peak-hour")
async def get_gross_margin():
    return analysis.peak_hour()

@app.get("/weekly-transactions")
async def get_weekly_transactions():
    return analysis.weekly_transactions()