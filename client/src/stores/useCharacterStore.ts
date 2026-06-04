import { create } from 'zustand';
import type { Character, AdvanceYearResponse, PendingEvent } from '../types/character';

interface CharacterState {
  characters: Character[];
  currentCharacter: Character | null;
  pendingEvents: PendingEvent[];
  yearResult: AdvanceYearResponse | null;
  setCharacters: (characters: Character[]) => void;
  setCurrentCharacter: (character: Character | null) => void;
  setPendingEvents: (events: PendingEvent[]) => void;
  setYearResult: (result: AdvanceYearResponse | null) => void;
  removePendingEvent: (eventId: number) => void;
}

export const useCharacterStore = create<CharacterState>((set) => ({
  characters: [],
  currentCharacter: null,
  pendingEvents: [],
  yearResult: null,

  setCharacters: (characters) => set({ characters }),
  setCurrentCharacter: (character) => set({ currentCharacter: character }),
  setPendingEvents: (events) => set({ pendingEvents: events }),
  setYearResult: (result) => set({ yearResult: result }),
  removePendingEvent: (eventId) =>
    set((state) => ({ pendingEvents: state.pendingEvents.filter((e) => e.id !== eventId) })),
}));
