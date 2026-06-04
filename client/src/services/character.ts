import { api } from './request';
import type { Character, CreateCharacterRequest, CharacterStats, AdvanceYearResponse } from '../types/character';

export const characterService = {
  create(data: CreateCharacterRequest) { return api.post<Character>('/characters', data); },
  getById(id: number) { return api.get<Character>(`/characters/${id}`); },
  getStats(id: number) { return api.get<CharacterStats>(`/characters/${id}/stats`); },
  advanceYear(id: number) { return api.post<AdvanceYearResponse>(`/characters/${id}/advance`); },
};
