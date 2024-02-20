<template>

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
export default {

  name: 'Users',
  data() {
			return {
				users: null,
        render: null,
			}
    },
  async mounted() {
    const request = await fetch('http://localhost:8000/predictmod/users/', {
      'Accept': 'application/json',
    })
    const userList = await request.json();
    console.log('---> Got user list: %s', JSON.stringify(userList));
    console.log('---> User list type: %s', typeof(userList));
    this.users = userList;
    this.render = true;
  },
  components: { UserList, DisclaimerShow, LicenseShow }
}
</script>
