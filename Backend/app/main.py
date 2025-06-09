# Backend/app/main.py
from fastapi import FastAPI
from .api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
import asyncio


app = FastAPI(
    title="Model Judge API",
    description="API for automatic chat/emotion evaluation",
    version="0.1.0"
)

from .model_loader import preload_model, sentence_model # Import from model_loader

@app.on_event("startup")
async def startup_event():
    await preload_model()

# 添加 CORS 中间件
origins = [
    "http://localhost:3000",  # For local React development
    "https://d99skwi58at3k.cloudfront.net", # For deployed React frontend
    "http://127.0.0.1:3000",
    # 你也可以根据需要添加其他允许的前端地址
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
