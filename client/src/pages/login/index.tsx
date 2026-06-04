import { View, Text, Button } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useAuthStore } from '../../stores/useAuthStore';
import { authService } from '../../services/auth';
import { getPlatform } from '../../utils/platform';
import './index.scss';

export default function Login() {
  const setAuth = useAuthStore((s) => s.setAuth);

  const handleWechatLogin = async () => {
    try {
      const { code } = await Taro.login();
      const result = await authService.wechatLogin({ code, platform: getPlatform() as 'wechat' });
      await setAuth(result.user, result.access_token, result.refresh_token);
      Taro.redirectTo({ url: '/pages/index/index' });
    } catch {
      Taro.showToast({ title: '登录失败', icon: 'error' });
    }
  };

  return (
    <View className='login-page'>
      <View className='login-page__header'>
        <Text className='login-page__title'>人生模拟器</Text>
        <Text className='login-page__subtitle'>观察 · 引导 · 见证一生</Text>
      </View>
      <View className='login-page__actions'>
        <Button className='login-page__btn' onClick={handleWechatLogin}>微信一键登录</Button>
      </View>
    </View>
  );
}
