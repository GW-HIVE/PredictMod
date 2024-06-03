// Utilities
import { defineStore } from 'pinia'

import axios from 'axios';

export const useAppStore = defineStore('app', {
    state: () => ({
      models: null,
      modelInitialSearch: [],
      dataPoints: null,
      targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/statistics/' : '/predictmod/api/statistics/',
      searchURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/search/' : '/predictmod/api/search/',
    }),
    actions: {
      reportState () {
        console.log("User App: Online");
      },
      async retrieveModelInfo() {
        const modelResponse = await axios.get(this.searchURL);
        this.modelInitialSearch = modelResponse.data;
        console.log("---> Retrieved model information: %s", modelResponse.data);
      },
    },
  });

