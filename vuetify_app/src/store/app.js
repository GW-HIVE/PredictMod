// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
    state: () => ({
      models: null,
      dataPoints: null,
      targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/statistics/' : '/predictmod/api/statistics/',
    }),
    actions: {
      reportState () {
        console.log("User App: Online");
      }
    }
  });

