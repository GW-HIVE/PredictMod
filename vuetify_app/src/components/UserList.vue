<template>

<v-table>
    <thead>
        <tr>
            <th class="text-center">
                First Name
            </th>
            <th class="text-center">
                Last Name
            </th>
            <th class="text-center">
                Email
            </th>
            <th class="text-center">
            </th>
            <th class="text-center">
            </th>
            <th class="text-center">
            </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="user in this.userList">
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td><a :href="user.url">{{ user.email }}</a></td>
            <td>
                <UpdatePassword :userID="user.id"/>
            </td>
            <td>
                <UpdateUser :userID="user.id" />
            </td>
            <td>
                <DeleteUser :userID="user.id" />
            </td>
        </tr>
    </tbody>
</v-table>

</template>

<script>

import { useUserStore } from '@/store/user';

import UpdateUser from '@/components/UpdateUser.vue';
import UpdatePassword from '@/components/UpdatePassword.vue';
import DeleteUser from '@/components/DeleterUser.vue';

export default {
    name: 'UserList',
    data: () => ({
        showUpdateUser: false,
        showUpdatePassword: false,
        showDeleteUser: false,
    }),
    props: {
        userList: Array,
    },
    setup() {
      const userStore = useUserStore();
      return { userStore };
    },
    components: { UpdatePassword, UpdateUser, DeleteUser }
}
</script>