import os
import uuid
import asyncio

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from dotenv import load_dotenv

from crewai import Crew, Process

from agent import (
    financial_analyst,
    verifier,
    risk_assessor,
    investment_advisor
)

from tasks import (
    verification,
    analyze_financial_document,
    risk_assessment,
    investment_analysis
)

# Load environment variables
load_dotenv()

app = FastAPI(title="Financial Document Analyzer")



# Multi-Agent Crew Definition

financial_crew = Crew(
    agents=[
        verifier,
        financial_analyst,
        risk_assessor,
        investment_advisor
    ],
    tasks=[
        verification,
        analyze_financial_document,
        risk_assessment,
        investment_analysis
    ],
    process=Process.sequential,
)


def run_crew(query: str, file_path: str):
    """
    Runs the full multi-agent financial analysis pipeline
    """
    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })
    return result



# API Endpoints

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Default query fallback
        if not query:
            query = "Analyze this financial document for investment insights"

        # Run Crew in background thread
        response = await asyncio.to_thread(
            run_crew,
            query.strip(),
            file_path
        )

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)