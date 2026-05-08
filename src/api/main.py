# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
security = HTTPBearer()

TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUDIENCE = os.getenv("AZURE_AUDIENCE")
SECRET_KEY = os.getenv("JWT_SECRET", "myjwtsecret")

OPENID_CONFIG = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"

# --- cache keys (avoid fetching on every request) ---
_jwks = None

def get_jwks():
    global _jwks
    if _jwks is None:
        config = requests.get(OPENID_CONFIG).json()
        jwks_uri = config["jwks_uri"]
        _jwks = requests.get(jwks_uri).json()
    return _jwks

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    # CI / test bypass
    if TEST_MODE:

        token = credentials.credentials

        # Simulate invalid token
        if token == "invalidtoken":
            raise HTTPException(status_code=403, detail="Invalid token")

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            return payload

        except Exception:
            raise HTTPException(status_code=403, detail="Invalid token")

    try:
        jwks = get_jwks()
        headers = jwt.get_unverified_header(token)

        key = next(k for k in jwks["keys"] if k["kid"] == headers["kid"])

        # Decode WITHOUT issuer validation first
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            options={"verify_iss": False}
        )

        # Now validate issuer manually (more flexible)
        issuer = payload.get("iss")

        valid_issuers = [
            f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
            f"https://sts.windows.net/{TENANT_ID}/"
        ]

        if issuer not in valid_issuers:
            raise HTTPException(status_code=403, detail="Invalid issuer")

        return payload

    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid Azure token: {str(e)}")
    
@app.get("/")
def health():
    return {"status": "running"}

@app.post("/run")
def trigger_pipeline(background_tasks: BackgroundTasks, user=Depends(verify_token)):
    print(f"USER PAYLOAD: {user}", flush=True)
    roles = user.get("roles", [])
    
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Admin role required")

    from src.workflows.run_pipeline import run_pipeline
    background_tasks.add_task(run_pipeline)

    return {"status": "pipeline started"}