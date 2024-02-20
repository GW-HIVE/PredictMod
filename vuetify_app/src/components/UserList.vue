<template>

<v-container class="text-center center">
    <v-col class="text-center center">
        <v-row class="text-center center">
            <v-btn @click.prevent()>
                New User?
            </v-btn>
        </v-row>
    </v-col>
</v-container>

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
                <v-btn @click.stop="showUpdatePassword=true">
                    Update Password
                    <UpdatePassword v-model="showUpdatePassword" />
                </v-btn>
            </td>
            <td>
                <v-btn @click.stop="showUpdateUser=true">
                    Update User
                    <UpdateUser v-model="showUpdateUser" />
                </v-btn>
            </td>
            <td>
                <v-btn @click.prevent()>Delete User</v-btn>
            </td>
        </tr>
    </tbody>
</v-table>

</template>

<script>

import UpdateUser from '@/components/UpdateUser.vue';
import UpdatePassword from '@/components/UpdatePassword.vue';

export default {
    name: 'UserList',
    data: () => ({
        showUpdateUser: false,
        showUpdatePassword: false,
    }),
    props: {
        userList: Array,
    },
    components: { UpdatePassword, UpdateUser }
}
</script>