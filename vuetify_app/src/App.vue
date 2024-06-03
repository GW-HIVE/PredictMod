<template>
    <!-- Vuetify documentation: https://vuetifyjs.com/en/components/tabs/ -->
    <!-- Also see SO at https://stackoverflow.com/questions/49721710/how-to-use-vuetify-tabs-with-vue-router -->
      <v-tabs height="48">
        <v-tab to="/predictmod/">Home</v-tab>
        <v-tab to="/predictmod/about">About</v-tab>
        <v-tab to="/predictmod/faq">FAQ</v-tab>
        <v-tab to="/predictmod/contact">Contact</v-tab>
        <v-tab to="/predictmod/query-builder">Query Builder</v-tab>
        <v-tab to="/predictmod/users">User Admin</v-tab>
        <v-tab to="/predictmod/help">Help</v-tab>
        <v-spacer></v-spacer>
          <v-col class="text-right ma-0 pa-0">
          <!-- TODO: Search input over countries scolls as expected, but the PredictMod values do not. 
              Toggle commenting to demonstrate.
          -->
          <SearchInput :items="this.appStore.modelInitialSearch" />
          <!-- <SearchInput /> -->
        </v-col>
        <v-tab to="/predictmod/login">{{ this.userStore.user ? `User: ${this.userStore.user}` : "Login" }}</v-tab>
      </v-tabs>

    <main>
      <router-view />
    </main>
</template>

<script>
import { ref } from 'vue';
import { useUserStore } from './store/user';
import { useAppStore } from '@/store/app';
import { useQueryState } from './store/queryState';
import SearchInput from '@/components/SearchInput';
import axios from 'axios';

// const searchValue = ref('')

export default {
    setup() {
      const queryState = useQueryState();
      const userStore = useUserStore();
      const appStore = useAppStore();
      return { queryState, userStore, appStore };
    },
    mounted() {
      // We must double-check user state on events like reload/refresh
      this.userStore.checkUser();
      this.appStore.reportState();
      this.appStore.retrieveModelInfo();
    },
    components: { SearchInput },
}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>