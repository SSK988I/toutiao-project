from fastapi import APIRouter

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_news_categories():
    # 这里可以添加获取新闻分类的逻辑
    return {"message": ["体育", "娱乐", "科技", "财经"]}