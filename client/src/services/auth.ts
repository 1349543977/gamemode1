import { api } from './request';
import type { LoginRequest, TokenResponse, User } from '../types/user';

export const authService = {
  wechatLogin(data: LoginRequest) { return api.post<TokenResponse>('/auth/wechat-login', data); },
  getProfile() { return api.get<User>('/auth/profile'); },
};
