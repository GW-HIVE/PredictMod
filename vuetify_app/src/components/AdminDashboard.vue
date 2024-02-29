<template>
      <h1>Administration</h1>
      <v-row class="justify-center">
        <v-btn variant="text" @click.prevent="users()">Users list</v-btn>
        <v-btn variant="text" @click.prevent="checkUser()">Who Am I</v-btn>
        <v-btn variant="text" @click="logState()">Log state to console</v-btn>
    </v-row>
</template>

<script>

import { useUserStore } from '@/store/user';

export default {
  name: 'AdminDashboard',
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  methods: {
    async checkUser() {
        const success = await this.userStore.checkUser();
        if (success) {
          // console.log();
        } else {
          console.log("Error when checking user status");
        }
      },
      users() {
        this.$router.push({ path: "/predictmod/users/" });
      },
      logState() {
        console.log("User state --->\n\tUser: %s\n\tCookie: %s", this.userStore.user, this.userStore.token);
        console.log("Store error: %s", this.userStore.error);
      },
  }
}

</script>