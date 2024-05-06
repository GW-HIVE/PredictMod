<template>
    <!-- Vuetify documentation: https://vuetifyjs.com/en/components/tabs/ -->
    <!-- Also see SO at https://stackoverflow.com/questions/49721710/how-to-use-vuetify-tabs-with-vue-router -->
      <v-tabs>
        <v-tab to="/predictmod/">Home</v-tab>
        <v-tab to="/predictmod/about">About</v-tab>
        <v-tab to="/predictmod/faq">FAQ</v-tab>
        <v-tab to="/predictmod/contact">Contact</v-tab>
        <v-tab to="/predictmod/query-builder">Query Builder</v-tab>
        <v-tab to="/predictmod/users">User Admin</v-tab>
        <v-tab to="/predictmod/help">Help</v-tab>
        <v-tab to="/predictmod/login">{{ this.userStore.user ? `User: ${this.userStore.user}` : "Login" }}</v-tab>
      </v-tabs>
    <main>
      <router-view />
    </main>
</template>

<script>
import { onMounted } from 'vue';
import { useUserStore } from './store/user';
import { useAppStore } from '@/store/app';
import { useQueryState } from './store/queryState';

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
    }

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