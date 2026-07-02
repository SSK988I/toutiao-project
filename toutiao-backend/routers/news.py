from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db 
from crud import news
from crud import news_cache

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news_cache.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "成功获取新闻分类列表",
        "data": categories
    }


@router.get("/list")
async def get_news_list(
    category_id: int = Query(..., alias="categoryId"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize", le=100),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db, category_id, offset, limit=page_size)
    total = await news.get_news_count(db, category_id)
    has_more = offset + page_size < total
    return {
        "code": 200,
        "message": "成功获取新闻列表",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        } 
    }

@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="newsId"), db = Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻未找到")
    
    views_increased = await news.increase_news_views(db, news_id)
    if not views_increased:
        raise HTTPException(status_code=500, detail="更新新闻浏览量失败")

    related_news = await news.get_related_news(db, news_detail.category_id, news_id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    
    }