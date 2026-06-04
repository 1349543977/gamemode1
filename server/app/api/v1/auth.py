from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt

from app.config import get_settings
from app.api.deps import get_user_repo, get_current_user
from app.domain.interfaces.repository import IUserRepository
from app.domain.entities.user import User
from app.schemas.auth import (
    WechatLoginRequest,
    PhoneBindRequest,
    TokenResponse,
    UserBrief,
    RefreshTokenRequest,
    UserProfileResponse,
)

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    return jwt.encode({"sub": str(user_id), "exp": expire, "type": "refresh"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


@router.post("/wechat-login", response_model=TokenResponse)
async def wechat_login(
    request: WechatLoginRequest,
    user_repo: IUserRepository = Depends(get_user_repo),
):
    openid = f"wx_{request.code}"
    user = await user_repo.get_by_openid(openid)
    if not user:
        user = User(
            openid=openid,
            nickname=f"玩家{openid[-4:]}",
            platform=request.platform,
            last_login_at=datetime.utcnow(),
        )
        user = await user_repo.create(user)
    else:
        user.last_login_at = datetime.utcnow()
        user = await user_repo.update(user)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
        user=UserBrief(
            id=user.id,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            has_phone=user.has_phone,
        ),
    )


@router.post("/phone-bind")
async def bind_phone(
    request: PhoneBindRequest,
    current_user: User = Depends(get_current_user),
    user_repo: IUserRepository = Depends(get_user_repo),
):
    current_user.phone = request.phone
    user = await user_repo.update(current_user)
    return {"message": "Phone bound successfully", "phone": user.phone}


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user_id = int(payload.get("sub"))
        access_token = create_access_token(user_id)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserProfileResponse(
        id=current_user.id,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        phone=current_user.phone,
        platform=current_user.platform,
        has_phone=current_user.has_phone,
    )
