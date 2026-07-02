# main.py
"""
EduGenie Learning Assistant - Backend (FastAPI)
Run locally with:
    uvicorn main:app --reload

Once running, open your browser at:
    http://127.0.0.1:8000        -> Welcome message / health check
    http://127.0.0.1:8000/docs   -> Interactive API docs (Swagger UI)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# ----------------------------------------------------------------------------
# App Initialization
# ----------------------------------------------------------------------------
app = FastAPI(
    title="EduGenie Learning Assistant",
    description="AI-powered educational backend for real-time learning support.",
    version="1.0.0"
)

# Allow frontend (running on a different port/origin) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # In production, restrict to specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# Data Models
# ----------------------------------------------------------------------------
class StudentQuery(BaseModel):
    student_name: str
    question: str

class QueryResponse(BaseModel):
    student_name: str
    question: str
    answer: str
    timestamp: str

# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """
    Root endpoint - confirms the backend is running.
    """
    return {
        "message": "EduGenie Learning Assistant backend is running successfully!",
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify server status.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/ask", response_model=QueryResponse)
def ask_question(query: StudentQuery):
    """
    Simulated AI educational response endpoint.
    Replace the logic below with actual AI model integration.
    """
    simulated_answer = (
        f"Hi {query.student_name}, here's a simple explanation for: "
        f"'{query.question}'. (Connect this endpoint to your AI model "
        f"to generate real educational answers.)"
    )

    return QueryResponse(
        student_name=query.student_name,
        question=query.question,
        answer=simulated_answer,
        timestamp=datetime.now().isoformat()
    )


# ----------------------------------------------------------------------------
# Run directly with `python main.py` (optional alternative to uvicorn CLI)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)