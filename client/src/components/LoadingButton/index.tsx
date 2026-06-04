import { View, Text } from '@tarojs/components';
import { PropsWithChildren } from 'react';
import './index.scss';

interface LoadingButtonProps extends PropsWithChildren {
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingButton({
  loading = false, disabled = false, onClick, children, variant = 'primary', size = 'md',
}: LoadingButtonProps) {
  return (
    <View
      className={`loading-btn loading-btn--${variant} loading-btn--${size} ${loading || disabled ? 'loading-btn--disabled' : ''}`}
      onClick={loading || disabled ? undefined : onClick}
    >
      {loading && <View className='loading-btn__spinner' />}
      <Text className='loading-btn__text'>{children}</Text>
    </View>
  );
}
