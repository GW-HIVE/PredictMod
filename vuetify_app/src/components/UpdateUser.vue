<template>
  <v-btn @click="dialog = true">
    Update User Profile
  </v-btn>
                <v-dialog width="512" v-model="dialog">
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Update User Profile</span>
                    </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
              <v-col>
                <v-text-field
                  label="First name"
                  v-model="firstName"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  label="Last name"
                  v-model="lastName"
                ></v-text-field>
              </v-col>
              </v-row>
              <v-row>
              <v-text-field
                  label="Email*"
                  required
                  v-model="email"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  label="Password*"
                  type="password"
                  required
                  v-model="password"
                ></v-text-field>
              </v-row>
                    </v-container>
          <v-container class="center">
           <v-row :v-if="myError">
              <p color="#ff0000">
                {{ myError }}
              </p>
          </v-row>
          </v-container>

                </v-card-text>
                <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="clearState()"
          >
            Cancel
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="submit()"
          >
            Save
                    </v-btn>
                </v-card-actions>
              </v-card>
    </v-dialog>
</template>

<script>
import { mapWritableState } from 'pinia';
import { useUserStore } from '@/store/user';

export default {
    name: 'UpdateUser',
    data: () => ({
        dialog: false,
        firstName: "",
        lastName: "",
        password: "",
        email: "",
        error: useUserStore().error,
    }),
    props: {
      userID: Number,
    },
    setup() {
      const userStore = useUserStore();
      return { userStore };
    },
    computed: {
      ...mapWritableState(useUserStore, {
        myError: "error"
      })
    },
    methods: {
      async submit() {
        const success = await this.userStore.updateProfile(
          this.userID, this.firstName, this.lastName, this.password, this.email
          );
        if (success) {
          this.clearState();
        }
      },
      clearState() {
        this.firstName = "",
        this.lastName = "",
        this.password = "",
        this.email = "",
        this.error = null;
        this.dialog = false;
      },
    }
}

</script>