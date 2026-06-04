import Taro from '@tarojs/taro';

export function getPlatform(): 'wechat' | 'ios' | 'android' | 'h5' {
  const env = Taro.getEnv();
  if (env === Taro.ENV_TYPE.WEAPP) return 'wechat';
  if (env === Taro.ENV_TYPE.WEB) return 'h5';
  return 'h5';
}

export function showToast(title: string, icon: 'success' | 'error' | 'none' = 'none', duration = 1500): void {
  Taro.showToast({ title, icon, duration });
}

export function showLoading(title = '加载中...'): void {
  Taro.showLoading({ title, mask: true });
}

export function hideLoading(): void {
  Taro.hideLoading();
}
