from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# 添加 CORS 中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)

if __name__ == "__main__":
    import uvicorn
    # reload=True 时必须传字符串 "main:app",不能传 app 对象,
    # 否则 uvicorn 无法在子进程里重新导入模块实现热重载。
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)