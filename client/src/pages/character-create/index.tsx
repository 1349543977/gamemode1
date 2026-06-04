import { View, Text, Input, Picker } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { useState, useEffect } from 'react';
import { characterService } from '../../services/character';
import { worldService } from '../../services/world';
import { useCharacterStore } from '../../stores/useCharacterStore';
import LoadingButton from '../../components/LoadingButton';
import type { City } from '../../types/world';
import './index.scss';

export default function CharacterCreate() {
  const [name, setName] = useState('');
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState(0);
  const [creating, setCreating] = useState(false);
  const { setCurrentCharacter } = useCharacterStore();

  useEffect(() => { loadCities(); }, []);

  const loadCities = async () => {
    try {
      const data = await worldService.getCities();
      setCities(data);
    } catch { Taro.showToast({ title: '加载城市失败', icon: 'error' }); }
  };

  const handleCreate = async () => {
    if (!name.trim()) { Taro.showToast({ title: '请输入角色姓名', icon: 'none' }); return; }
    if (cities.length === 0) { Taro.showToast({ title: '请选择出生城市', icon: 'none' }); return; }
    try {
      setCreating(true);
      const character = await characterService.create({ name: name.trim(), gender, city_id: cities[selectedCity].id });
      setCurrentCharacter(character);
      Taro.redirectTo({ url: `/pages/game/index?characterId=${character.id}` });
    } catch { Taro.showToast({ title: '创建失败', icon: 'error' }); }
    finally { setCreating(false); }
  };

  return (
    <View className='create-page'>
      <Text className='create-page__title'>创建新角色</Text>
      <View className='create-page__form'>
        <View className='form-field'>
          <Text className='form-field__label'>姓名</Text>
          <Input className='form-field__input' placeholder='给角色取个名字' value={name} onInput={(e) => setName(e.detail.value)} maxlength={20} />
        </View>
        <View className='form-field'>
          <Text className='form-field__label'>性别</Text>
          <Picker mode='selector' range={['男', '女']} value={gender === 'male' ? 0 : 1} onChange={(e) => setGender(e.detail.value === 0 ? 'male' : 'female')}>
            <View className='form-field__picker'>{gender === 'male' ? '男' : '女'}</View>
          </Picker>
        </View>
        <View className='form-field'>
          <Text className='form-field__label'>出生城市</Text>
          <Picker mode='selector' range={cities.map((c) => c.name)} value={selectedCity} onChange={(e) => setSelectedCity(Number(e.detail.value))}>
            <View className='form-field__picker'>{cities[selectedCity]?.name || '选择城市'}</View>
          </Picker>
        </View>
      </View>
      <LoadingButton variant='primary' size='lg' loading={creating} onClick={handleCreate}>开始人生</LoadingButton>
    </View>
  );
}
