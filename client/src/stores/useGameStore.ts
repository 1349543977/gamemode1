import { create } from 'zustand';

interface GameState {
  isAdvancing: boolean;
  showYearSummary: boolean;
  darkMode: boolean;
  setIsAdvancing: (value: boolean) => void;
  setShowYearSummary: (show: boolean) => void;
  toggleDarkMode: () => void;
}

export const useGameStore = create<GameState>((set) => ({
  isAdvancing: false,
  showYearSummary: false,
  darkMode: false,

  setIsAdvancing: (value) => set({ isAdvancing: value }),
  setShowYearSummary: (show) => set({ showYearSummary: show }),
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
}));
