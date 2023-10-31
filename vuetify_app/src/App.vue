<template>
    <!-- Vuetify documentation: https://vuetifyjs.com/en/components/tabs/ -->
    <!-- Also see SO at https://stackoverflow.com/questions/49721710/how-to-use-vuetify-tabs-with-vue-router -->
    <v-tabs>
      <v-tab to="/predictmod/">Home</v-tab>
      <v-tab to="/predictmod/about">About</v-tab>
      <v-tab to="/predictmod/faq">FAQ</v-tab>
      <v-tab to="/predictmod/contact">Contact</v-tab>
      <v-tab to="/predictmod/login">Login</v-tab>
    </v-tabs>
    <main>
      <router-view />
    </main>
</template>

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