from fastapi import FastAPI, Header, HTTPException
from src.workflows.run_pipeline import run_pipeline
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/run")
def trigger_pipeline(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = run_pipeline()
    return result
