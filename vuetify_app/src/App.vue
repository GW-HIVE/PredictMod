<template>
    <!-- Vuetify documentation: https://vuetifyjs.com/en/components/tabs/ -->
    <!-- Also see SO at https://stackoverflow.com/questions/49721710/how-to-use-vuetify-tabs-with-vue-router -->
    <v-tabs>
      <v-tab to="/predictmod-beta/">Home</v-tab>
      <v-tab to="/predictmod-beta/about">About</v-tab>
      <v-tab to="/predictmod-beta/faq">FAQ</v-tab>
      <v-tab to="/predictmod-beta/contact">Contact</v-tab>
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