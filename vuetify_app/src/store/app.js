// Utilities
import { defineStore } from 'pinia'

import axios from 'axios';

function convertModelName(name) {
  return name.replace(/[_-]/g, ' ')
}

export const useAppStore = defineStore('app', {
    state: () => ({
      releasedModels: null,
      pendingModels: null,
      modelInitialSearch: [],
      dataPoints: null,
      targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/statistics/' : '/predictmod/api/statistics/',
      searchURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/search/' : '/predictmod/api/search/',
      modelsURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/models/': "/predictmod/api/models/",

    }),
    actions: {
      reportState () {
        console.log("User App: Online");
      },
      async getModels() {
        console.log("---> App Store: Getting models! <---")
        const response = await axios.get(this.modelsURL);
        if (!response.status === 200) {
          console.log("---> Error!\n%s", response.status);
        } else {
          // console.log("---> Home: Got response\n", JSON.stringify(response.data))
          const releasedModels = JSON.parse(response.data.released_models);
          releasedModels.forEach(model => {
            model.fields.name = convertModelName(model.fields.name)
          });
          this.releasedModels = releasedModels;

          const pendingModels = JSON.parse(response.data.pending_models);
          pendingModels.forEach(model => {
            model.fields.name = convertModelName(model.fields.name)
          })
          this.pendingModels = pendingModels;
        }
      },
      async retrieveModelInfo() {
        const modelResponse = await axios.get(this.searchURL);
        this.modelInitialSearch = modelResponse.data;
        // console.log("---> Retrieved model information: %s", JSON.stringify(modelResponse.data));
      },
    },
});

