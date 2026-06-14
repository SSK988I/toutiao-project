from fastapi import FastAPI
from routers import news
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)

if __name__ == "__main__":
    import uvicorn
    # reload=True 时必须传字符串 "main:app",不能传 app 对象,
    # 否则 uvicorn 无法在子进程里重新导入模块实现热重载。
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)