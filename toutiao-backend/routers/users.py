from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from crud.users import create_token, get_user_by_username, create_user, authenticate_user, update_user, change_password
from starlette import status
from utils.response import success_response
from utils.auth import get_current_user
from models.users import User
router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    get_user = await get_user_by_username(db, user_data.username)
    if get_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    new_user = await create_user(db, user_data)
    token = await create_token(db, new_user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(new_user))

    return success_response(message="注册成功", data=response_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户或密码错误")
    token = await create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))

    return success_response(message="登录成功", data=response_data)

@router.get("/info")
async def get_user_info(user: User =Depends(get_current_user)):

    return success_response(
        message="获取用户信息成功",
        data=UserInfoResponse.model_validate(user)   # 复用注册/登录同款响应模型
    )

@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User =Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await update_user(db, user.username, user_data)
    
    return success_response(
        message="用户信息更新成功",
        data=UserInfoResponse.model_validate(user)   # 复用注册/登录同款响应模型
    )

@router.put("/password")
async def update_password(
    password_data:UserChangePasswordRequest,
    user: User =Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res_change_pwd = await change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败")
    return success_response(
        message="密码修改成功",
    )