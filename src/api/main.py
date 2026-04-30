from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.workflows.run_pipeline import run_pipeline
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

app = FastAPI()

# -----------------------------
# Security setup (JWT)
# -----------------------------
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "myjwtsecret")  # dev fallback
ALGORITHM = "HS256"


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def health():
    return {"status": "running"}


# -----------------------------
# Secure pipeline trigger
# -----------------------------
@app.post("/run")
def trigger_pipeline(
    background_tasks: BackgroundTasks,
    user=Depends(verify_token)
):
    background_tasks.add_task(run_pipeline)

    return {
        "status": "pipeline started",
        "user": user
    }