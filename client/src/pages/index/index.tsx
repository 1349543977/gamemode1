import { View, Text } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useEffect, useState } from 'react';
import { useAuthStore } from '../../stores/useAuthStore';
import { useCharacterStore } from '../../stores/useCharacterStore';
import CharacterCard from '../../components/CharacterCard';
import LoadingButton from '../../components/LoadingButton';
import './index.scss';

export default function Index() {
  const [loading, setLoading] = useState(true);
  const user = useAuthStore((s) => s.user);
  const { characters, setCharacters, setCurrentCharacter } = useCharacterStore();

  useEffect(() => {
    // MVP: 暂无列表API，显示空列表
    setCharacters([]);
    setLoading(false);
  }, []);

  const handleCharacterClick = (id: number) => {
    const char = characters.find((c) => c.id === id);
    if (char) setCurrentCharacter(char);
    Taro.navigateTo({ url: `/pages/game/index?characterId=${id}` });
  };

  const handleCreateNew = () => {
    Taro.navigateTo({ url: '/pages/character-create/index' });
  };

  return (
    <View className='index-page'>
      <View className='index-page__header'>
        <Text className='index-page__greeting'>你好，{user?.nickname || '玩家'}</Text>
        <Text className='index-page__subtitle'>选择一个角色开始人生</Text>
      </View>
      {loading ? (
        <View className='index-page__skeleton'>
          {[1, 2, 3].map((i) => <View key={i} className='skeleton-card' />)}
        </View>
      ) : (
        <View className='index-page__list'>
          {characters.map((char) => <CharacterCard key={char.id} character={char} onClick={handleCharacterClick} />)}
          {characters.length === 0 && <Text className='index-page__empty'>还没有角色，创建一个开始人生吧</Text>}
        </View>
      )}
      <View className='index-page__footer'>
        <LoadingButton variant='primary' size='lg' onClick={handleCreateNew}>创建新角色</LoadingButton>
      </View>
    </View>
  );
}
