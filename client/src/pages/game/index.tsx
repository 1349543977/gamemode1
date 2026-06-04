import { View, Text } from '@tarojs/components';
import Taro, { useRouter } from '@tarojs/taro';
import { useEffect, useState, useCallback } from 'react';
import { characterService } from '../../services/character';
import { eventService } from '../../services/event';
import { useCharacterStore } from '../../stores/useCharacterStore';
import { useGameStore } from '../../stores/useGameStore';
import AttributeRadar from '../../components/AttributeRadar';
import EventCard from '../../components/EventCard';
import YearSummaryModal from '../../components/YearSummaryModal';
import LoadingButton from '../../components/LoadingButton';
import './index.scss';

const STAGE_LABELS: Record<string, string> = {
  infant: '婴儿期', toddler: '幼儿期', childhood: '少年期',
  adolescence: '青春期', youth: '青年期', prime: '壮年期',
  middle_age: '中年期', elderly: '老年期',
};

export default function Game() {
  const router = useRouter();
  const characterId = Number(router.params.characterId || 0);
  const currentCharacter = useCharacterStore((s) => s.currentCharacter);
  const setCurrentCharacter = useCharacterStore((s) => s.setCurrentCharacter);
  const pendingEvents = useCharacterStore((s) => s.pendingEvents);
  const setPendingEvents = useCharacterStore((s) => s.setPendingEvents);
  const yearResult = useCharacterStore((s) => s.yearResult);
  const setYearResult = useCharacterStore((s) => s.setYearResult);
  const removePendingEvent = useCharacterStore((s) => s.removePendingEvent);
  const isAdvancing = useGameStore((s) => s.isAdvancing);
  const setIsAdvancing = useGameStore((s) => s.setIsAdvancing);
  const showYearSummary = useGameStore((s) => s.showYearSummary);
  const setShowYearSummary = useGameStore((s) => s.setShowYearSummary);
  const [activeTab, setActiveTab] = useState<'map' | 'stats' | 'records' | 'settings'>('map');
  const [choosingEvent, setChoosingEvent] = useState(false);

  useEffect(() => { if (characterId) loadCharacter(); }, [characterId]);

  const loadCharacter = async () => {
    try {
      const char = await characterService.getById(characterId);
      setCurrentCharacter(char);
    } catch { Taro.showToast({ title: '加载失败', icon: 'error' }); }
  };

  const handleAdvanceYear = useCallback(async () => {
    if (!characterId || isAdvancing) return;
    try {
      setIsAdvancing(true);
      const result = await characterService.advanceYear(characterId);
      setYearResult(result);
      setPendingEvents(result.pending_events);
      if (result.character.is_alive) await loadCharacter();
      if (result.pending_events.length === 0) setShowYearSummary(true);
    } catch { Taro.showToast({ title: '推进失败', icon: 'error' }); }
    finally { setIsAdvancing(false); }
  }, [characterId, isAdvancing]);

  const handleEventChoose = useCallback(async (eventId: number, choiceIndex: number) => {
    if (!characterId || choosingEvent) return;
    try {
      setChoosingEvent(true);
      await eventService.chooseOption(eventId, { character_id: characterId, choice_index: choiceIndex });
      removePendingEvent(eventId);
      await loadCharacter();
      if (pendingEvents.length <= 1) setShowYearSummary(true);
    } catch { Taro.showToast({ title: '选择失败', icon: 'error' }); }
    finally { setChoosingEvent(false); }
  }, [characterId, choosingEvent, pendingEvents.length]);

  const handleCloseSummary = useCallback(() => { setShowYearSummary(false); setYearResult(null); }, []);

  if (!currentCharacter) return <View className='game-page'><Text>加载中...</Text></View>;

  return (
    <View className='game-page'>
      <View className='game-page__header'>
        <View className='game-page__char-info'>
          <Text className='game-page__char-name'>{currentCharacter.name}</Text>
          <Text className='game-page__char-age'>{currentCharacter.age}岁</Text>
        </View>
        <Text className='game-page__char-stage'>{STAGE_LABELS[currentCharacter.stage] || currentCharacter.stage}</Text>
      </View>
      {pendingEvents.length > 0 && (
        <View className='game-page__events'>
          <Text className='game-page__events-title'>待处理事件</Text>
          {pendingEvents.map((event) => <EventCard key={event.id} event={event} onChoose={handleEventChoose} loading={choosingEvent} />)}
        </View>
      )}
      <View className='game-page__content'>
        {activeTab === 'map' && <View className='game-page__map'><Text className='game-page__map-placeholder'>{currentCharacter.city?.name || '未知城市'}</Text></View>}
        {activeTab === 'stats' && currentCharacter.stats && <AttributeRadar stats={currentCharacter.stats} />}
        {activeTab === 'records' && <View className='game-page__records'><Text className='text-secondary'>人生记录将在这里显示</Text></View>}
        {activeTab === 'settings' && <View className='game-page__settings'><Text className='text-secondary'>游戏设置</Text></View>}
      </View>
      <View className='game-page__footer'>
        <View className='game-page__tabs'>
          {(['map', 'stats', 'records', 'settings'] as const).map((tab) => (
            <View key={tab} className={`game-page__tab ${activeTab === tab ? 'game-page__tab--active' : ''}`} onClick={() => setActiveTab(tab)}>
              <Text>{{ map: '地图', stats: '属性', records: '记录', settings: '设置' }[tab]}</Text>
            </View>
          ))}
        </View>
        {currentCharacter.is_alive && pendingEvents.length === 0 && (
          <LoadingButton variant='primary' size='lg' loading={isAdvancing} onClick={handleAdvanceYear}>度过这一年</LoadingButton>
        )}
      </View>
      {showYearSummary && yearResult && <YearSummaryModal result={yearResult} onClose={handleCloseSummary} />}
    </View>
  );
}
