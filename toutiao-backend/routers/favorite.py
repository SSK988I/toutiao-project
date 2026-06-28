from fastapi import HTTPException, status, APIRouter, Query, Depends
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse
from crud.favorite import add_news_favorite, get_favorites_list, is_news_favorite, remove_all_favorites, remove_news_favorite
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db

from utils.auth import get_current_user

from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    is_favorite = await is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorite))


@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加收藏
    """
    news_id = data.news_id
    result = await add_news_favorite(db, user.id, news_id)
    await db.commit()
    return success_response(message="添加收藏成功", data=result)

@router.delete("/remove")
async def delete_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    is_removed = await remove_news_favorite(db, user.id, news_id)
    if not is_removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除收藏失败")
    return success_response(message="删除收藏成功")

@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取收藏列表
    """
    rows, total = await get_favorites_list(db, user.id, page, page_size)
    favorite_list = [ {
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id,
    } for news, favorite_time, favorite_id in rows]
    has_more = total > page * page_size
    data = FavoriteListResponse(total=total, hasMore=has_more, List=favorite_list)
    return success_response(message="获取收藏列表成功", data=data)


@router.delete("/clear")
async def clear_favorite(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    清空用户收藏记录
    """
    count = await remove_all_favorites(db, user.id)
    return success_response(message=f"清空了{count}条收藏记录")
