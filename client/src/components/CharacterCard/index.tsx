import { View, Text } from '@tarojs/components';
import type { Character } from '../../types/character';
import './index.scss';

interface CharacterCardProps {
  character: Character;
  onClick?: (id: number) => void;
}

const STAGE_LABELS: Record<string, string> = {
  infant: '婴儿期', toddler: '幼儿期', childhood: '少年期',
  adolescence: '青春期', youth: '青年期', prime: '壮年期',
  middle_age: '中年期', elderly: '老年期',
};

export default function CharacterCard({ character, onClick }: CharacterCardProps) {
  return (
    <View className='character-card' onClick={() => onClick?.(character.id)}>
      <View className='character-card__header'>
        <Text className='character-card__name'>{character.name}</Text>
        <Text className={`character-card__status ${character.is_alive ? 'character-card__status--alive' : 'character-card__status--dead'}`}>
          {character.is_alive ? '存活' : '已故'}
        </Text>
      </View>
      <View className='character-card__info'>
        <Text className='character-card__age'>{character.age}岁</Text>
        <Text className='character-card__stage'>{STAGE_LABELS[character.stage] || character.stage}</Text>
        {character.city && <Text className='character-card__city'>{character.city.name}</Text>}
      </View>
      {character.stats && (
        <View className='character-card__stats'>
          <View className='stat-bar'><Text className='stat-bar__label'>健康</Text><View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.health}%`, background: 'var(--color-success)' }} /></View></View>
          <View className='stat-bar'><Text className='stat-bar__label'>智力</Text><View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.intelligence}%`, background: 'var(--color-primary)' }} /></View></View>
          <View className='stat-bar'><Text className='stat-bar__label'>魅力</Text><View className='stat-bar__track'><View className='stat-bar__fill' style={{ width: `${character.stats.charisma}%`, background: 'var(--color-secondary)' }} /></View></View>
        </View>
      )}
    </View>
  );
}
