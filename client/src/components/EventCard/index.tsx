import { View, Text } from '@tarojs/components';
import type { PendingEvent } from '../../types/character';
import LoadingButton from '../LoadingButton';
import './index.scss';

interface EventCardProps {
  event: PendingEvent;
  onChoose: (eventId: number, choiceIndex: number) => void;
  loading?: boolean;
}

export default function EventCard({ event, onChoose, loading = false }: EventCardProps) {
  return (
    <View className='event-card'>
      <View className='event-card__header'><Text className='event-card__title'>{event.title}</Text></View>
      <Text className='event-card__description'>{event.description}</Text>
      <View className='event-card__choices'>
        {event.choices.map((choice) => (
          <LoadingButton key={choice.index} variant='secondary' size='md' loading={loading}
            onClick={() => onChoose(event.id, choice.index)}>
            {choice.text}
          </LoadingButton>
        ))}
      </View>
    </View>
  );
}
