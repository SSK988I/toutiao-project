from datetime import datetime

from schemas.base import NewsItemBase
from pydantic import ConfigDict, Field
from pydantic import BaseModel

class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

class FavoriteNewsItemBase(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )




class FavoriteListResponse(BaseModel):
    total: int = Field()
    hasMore: bool = Field(..., alias="hasMore")
    List: list[FavoriteNewsItemBase] = Field(..., alias="list")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
