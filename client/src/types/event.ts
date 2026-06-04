export interface EventChoiceRequest {
  character_id: number;
  choice_index: number;
}

export interface EventChoiceResult {
  narrative: string;
  effects: Record<string, number>;
  new_stats: { health: number; intelligence: number; charisma: number; wealth: number; happiness: number; luck: number };
  triggered_events: { id: number; title: string; description: string }[];
}
