import Taro from '@tarojs/taro';

export const storage = {
  async get(key: string): Promise<string | null> {
    try {
      const value = await Taro.getStorageSync(key);
      return value || null;
    } catch { return null; }
  },
  async set(key: string, value: string): Promise<void> {
    try { await Taro.setStorageSync(key, value); } catch (e) { console.error(`Storage set error: ${key}`, e); }
  },
  async remove(key: string): Promise<void> {
    try { await Taro.removeStorageSync(key); } catch (e) { console.error(`Storage remove error: ${key}`, e); }
  },
};
