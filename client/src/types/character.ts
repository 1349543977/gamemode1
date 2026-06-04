export interface CharacterStats {
  health: number;
  intelligence: number;
  charisma: number;
  wealth: number;
  happiness: number;
  luck: number;
}

export interface Character {
  id: number;
  name: string;
  gender: 'male' | 'female';
  age: number;
  stage: string;
  is_alive: boolean;
  city: { id: number; name: string } | null;
  stats: CharacterStats | null;
}

export interface CreateCharacterRequest {
  name: string;
  gender: 'male' | 'female';
  city_id: number;
}

export interface PendingEvent {
  id: number;
  title: string;
  description: string;
  choices: { index: number; text: string }[];
}

export interface AdvanceYearResponse {
  character: { age: number; stage: string; is_alive: boolean };
  year_summary: { stat_changes: Record<string, number>; stage_changed: boolean; death_cause: string | null };
  pending_events: PendingEvent[];
}
