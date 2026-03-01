from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import StepInput
from reasoning_engine import analyze_reasoning
from modules.multi_agent import multi_agent_analysis
from modules.pdf_export import generate_pdf


app = FastAPI(title="CognitiveMirror API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "CognitiveMirror backend running"}

@app.post("/analyze")
def analyze(data: StepInput):
    try:
        result = analyze_reasoning(data)
        return result
    except Exception as e:
        print("ERROR:", str(e))  # prints in terminal
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/compare")
def compare_agents(data: StepInput):
    return multi_agent_analysis(data) 

@app.post("/export")
def export_report(data: StepInput):
    return generate_pdf(data)   