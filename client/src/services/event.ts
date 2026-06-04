import { api } from './request';
import type { EventChoiceRequest, EventChoiceResult } from '../types/event';
import type { PendingEvent } from '../types/character';

export const eventService = {
  getPendingEvents(characterId: number) { return api.get<PendingEvent[]>(`/events/pending/${characterId}`); },
  chooseOption(eventId: number, data: EventChoiceRequest) { return api.post<EventChoiceResult>(`/events/${eventId}/choose`, data); },
};
