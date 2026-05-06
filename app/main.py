from fastapi import FastAPI
from app.routers.review import router
from app.core.config import settings
from app.auth.jwt_handler import create_access_token

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "LLM Code Reviewer API", "docs": "/docs"}

@app.post("/token")
async def get_token(username: str = "demo"):
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
