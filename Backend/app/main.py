# Backend/app/main.py
from fastapi import FastAPI
from app.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Model Judge API",
    description="API for automatic chat/emotion evaluation",
    version="0.1.0"
)

# 添加 CORS 中间件
origins = [
    "http://localhost:3000",
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
