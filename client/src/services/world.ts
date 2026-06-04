import { api } from './request';
import type { City, WorldState } from '../types/world';

export const worldService = {
  getWorldState() { return api.get<WorldState>('/world/state'); },
  getCities() { return api.get<City[]>('/world/cities'); },
};
