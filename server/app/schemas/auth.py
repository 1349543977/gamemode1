from pydantic import BaseModel, Field
from typing import Optional


class WechatLoginRequest(BaseModel):
    code: str = Field(..., min_length=1, description="微信登录code")
    platform: str = Field(default="wechat", pattern="^(wechat|ios|android)$")


class PhoneBindRequest(BaseModel):
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    verify_code: str = Field(..., min_length=4, max_length=6, description="验证码")


class UserBrief(BaseModel):
    id: int
    nickname: str
    avatar_url: Optional[str] = None
    has_phone: bool


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserBrief


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserProfileResponse(BaseModel):
    id: int
    nickname: str
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    platform: str
    has_phone: bool
