export interface City {
  id: number;
  name: string;
  region: string;
  population: number;
  development_index: number;
  cost_of_living: number;
}

export interface WorldState {
  year: number;
  era: string;
  gdp_index: number;
  tech_level: number;
  major_events: string[] | null;
}
