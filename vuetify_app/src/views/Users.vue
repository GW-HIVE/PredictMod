<template>

<!--
<v-container class="text-center center">
    <v-col class="text-center center">
        <v-row class="text-center center">
            <v-btn type="submit" @click.prevent="redirect()">
                New User?
            </v-btn>
        </v-row>
    </v-col>
</v-container>
-->

  <v-col v-if="render">
    <UserList :user-list="users" />
  </v-col>

    <v-row>
      <v-col>
        <DisclaimerShow/>
      </v-col>
      <v-col>
        <LicenseShow/>
      </v-col>
    </v-row>



</template>
<script>

import DisclaimerShow from './DisclaimerShow.vue';
import LicenseShow from './LicenseShow.vue';
import UserList from '@/components/UserList.vue';

const baseURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/users/': "/predictmod/api/users/";

export default {

  name: 'Users',
  data() {
			return {
				users: null,
        render: null,
			}
    },
  async mounted() {
    const request = await fetch(baseURL, {
      'Accept': 'application/json',
      credentials: 'include',
    })
    const userList = await request.json();
    // console.log('---> Got user list: %s', JSON.stringify(userList));
    // console.log('---> User list type: %s', typeof(userList));
    if ("error" in userList) {
      alert(userList["error"]);
      return;
    }
    this.users = userList;
    this.render = true;
  },
  methods: {
    redirect() {
      this.$router.push({ path: "/predictmod/login" });
    }
  },
  components: { UserList, DisclaimerShow, LicenseShow }
}
</script>
