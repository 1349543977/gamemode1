import { View, Text } from '@tarojs/components';
import type { AdvanceYearResponse } from '../../types/character';
import LoadingButton from '../LoadingButton';
import './index.scss';

interface YearSummaryModalProps {
  result: AdvanceYearResponse;
  onClose: () => void;
}

const STAT_LABELS: Record<string, string> = {
  health: '健康', intelligence: '智力', charisma: '魅力',
  wealth: '财富', happiness: '幸福', luck: '运气',
};

export default function YearSummaryModal({ result, onClose }: YearSummaryModalProps) {
  const { character, year_summary } = result;
  return (
    <View className='year-summary'>
      <View className='year-summary__overlay' onClick={onClose} />
      <View className='year-summary__content'>
        <Text className='year-summary__title'>{character.age}岁年度总结</Text>
        {year_summary.stage_changed && (
          <View className='year-summary__milestone'><Text className='year-summary__milestone-text'>人生进入新阶段！</Text></View>
        )}
        <View className='year-summary__changes'>
          <Text className='year-summary__section-title'>属性变化</Text>
          {Object.entries(year_summary.stat_changes).map(([key, value]) => (
            <View className='year-summary__change-row' key={key}>
              <Text className='year-summary__change-label'>{STAT_LABELS[key] || key}</Text>
              <Text className={`year-summary__change-value ${value > 0 ? 'year-summary__change-value--up' : value < 0 ? 'year-summary__change-value--down' : ''}`}>
                {value > 0 ? `+${value}` : String(value)}
              </Text>
            </View>
          ))}
        </View>
        {year_summary.death_cause && (
          <View className='year-summary__death'><Text className='year-summary__death-text'>角色因"{year_summary.death_cause}"离世</Text></View>
        )}
        <LoadingButton variant='primary' size='lg' onClick={onClose}>继续</LoadingButton>
      </View>
    </View>
  );
}
