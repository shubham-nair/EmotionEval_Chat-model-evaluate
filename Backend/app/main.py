# Backend/app/main.py
from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Model Judge API",
    description="API for automatic chat/emotion evaluation",
    version="0.1.0"
)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
