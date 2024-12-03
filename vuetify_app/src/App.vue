<template v-slot:extension>
    <!-- Vuetify documentation: https://vuetifyjs.com/en/components/tabs/ -->
    <!-- Also see SO at https://stackoverflow.com/questions/49721710/how-to-use-vuetify-tabs-with-vue-router -->
    <!-- <template v-slot:extension> -->
      <v-tabs height="48">

        <v-tab
          v-for="link in links"
          :text="link.name"
          :to="link.to"
        ></v-tab>

        <v-menu>
          <template v-slot:activator="{ props }">
          <v-btn 
            class="align-self-center"
            height="100%"
            rounded="0"
            variant="plain"
            v-bind="props"
            >
            More
            <v-icon icon="mdi-menu-down" end></v-icon>
          </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="item in modelMenu"
              :key="item.name"
              :title="item.name"
              @click="routeTo(item.to)"
              >
          
            </v-list-item>
          </v-list>
        </v-menu>
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
    <!-- </template> -->
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
import { templateSettings } from 'lodash';

// const searchValue = ref('')

export default {
    setup() {
      const queryState = useQueryState();
      const userStore = useUserStore();
      const appStore = useAppStore();
      return { queryState, userStore, appStore };
    },
    data: () => ({
      links: [
        { name: "Home", to: "/predictmod/" },
        { name: "About", to:  "/predictmod/about" },
        { name: "FAQ", to: "/predictmod/faq" },
        { name: "Contact", to:  "/predictmod/contact" },
        { name: "Query Builder", to: "/predictmod/query-builder" },
        { name: "Models", to:  "/predictmod/models" },
        { name: "Users", to:  "/predictmod/users" },
        { name: "Help", to: "/predictmod/help" },
      ],
      modelMenu: [
        { name: "Automated Pipeline", to: "/predictmod/autmoated-pipeline" },
        { name: "AI/ML Tutorial", to: "/predictmod/tutorial" },
        { name: "New Models", to: "/predictmod/new-models" },
      ]
    }),
    mounted() {
      // We must double-check user state on events like reload/refresh
      this.userStore.checkUser();
      this.appStore.reportState();
      this.appStore.retrieveModelInfo();
    },
    methods: {
      routeTo(newLocation) {
        this.$router.push(newLocation);
      }
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