import { View, Text } from '@tarojs/components';
import type { CharacterStats } from '../../types/character';
import './index.scss';

interface AttributeRadarProps {
  stats: CharacterStats;
}

const STAT_CONFIG = [
  { key: 'health' as const, label: '健康', color: '#10B981' },
  { key: 'intelligence' as const, label: '智力', color: '#6366F1' },
  { key: 'charisma' as const, label: '魅力', color: '#8B5CF6' },
  { key: 'wealth' as const, label: '财富', color: '#F59E0B' },
  { key: 'happiness' as const, label: '幸福', color: '#EC4899' },
  { key: 'luck' as const, label: '运气', color: '#3B82F6' },
];

export default function AttributeRadar({ stats }: AttributeRadarProps) {
  return (
    <View className='attribute-radar'>
      {STAT_CONFIG.map(({ key, label, color }) => (
        <View className='attribute-radar__row' key={key}>
          <Text className='attribute-radar__label'>{label}</Text>
          <View className='attribute-radar__track'>
            <View className='attribute-radar__fill' style={{ width: `${stats[key]}%`, backgroundColor: color }} />
          </View>
          <Text className='attribute-radar__value'>{stats[key]}</Text>
        </View>
      ))}
    </View>
  );
}
