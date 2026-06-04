export interface User {
  id: number;
  nickname: string;
  avatar_url: string | null;
  phone: string | null;
  platform: string;
  has_phone: boolean;
}

export interface LoginRequest {
  code: string;
  platform: 'wechat' | 'ios' | 'android';
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}
