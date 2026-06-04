import Taro from '@tarojs/taro';
import { storage } from '../utils/storage';

const BASE_URL = process.env.TARO_APP_API_URL || '/api/v1';

interface RequestOptions {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: unknown;
}

class Request {
  private baseUrl: string;
  constructor(baseUrl: string) { this.baseUrl = baseUrl; }

  private async getAuthHeader(): Promise<Record<string, string>> {
    const token = await storage.get('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async request<T>(options: RequestOptions): Promise<T> {
    const authHeader = await this.getAuthHeader();
    const response = await Taro.request({
      url: `${this.baseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: { 'Content-Type': 'application/json', ...authHeader },
    });
    if (response.statusCode === 401) {
      await storage.remove('access_token');
      Taro.redirectTo({ url: '/pages/login/index' });
      throw new Error('Unauthorized');
    }
    if (response.statusCode >= 400) {
      throw new Error(response.data?.error?.message || response.data?.detail || 'Request failed');
    }
    return response.data as T;
  }

  get<T>(url: string) { return this.request<T>({ url, method: 'GET' }); }
  post<T>(url: string, data?: unknown) { return this.request<T>({ url, method: 'POST', data }); }
  put<T>(url: string, data?: unknown) { return this.request<T>({ url, method: 'PUT', data }); }
  delete<T>(url: string) { return this.request<T>({ url, method: 'DELETE' }); }
}

export const api = new Request(BASE_URL);
