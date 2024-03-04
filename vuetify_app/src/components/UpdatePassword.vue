<template>
      <v-btn @click="dialog = true">
        Update Password
      </v-btn>
          <v-dialog width="512" v-model="dialog">
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Update Password</span>
                    </v-card-title>
                <v-card-text>
                    <v-container>
                            <v-row>
                <v-text-field
                  label="Old password*"
                  v-model="oldPassword"
                  required
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  label="New password*"
                  v-model="newPassword"
                  required
                  ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  label="Retype new password"
                  v-model="repeatNewPassword"
                ></v-text-field>
                <!-- type="password" -->
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
          <v-container class="center">
            <v-row>
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
          <!-- <v-btn variant="text" @click="logState()">
            Log state to console
          </v-btn> -->
                  </v-row>
                  </v-container>
                </v-card-actions>
              </v-card>
    </v-dialog>
</template>

<script>
import { mapWritableState } from 'pinia';
import { useUserStore } from '@/store/user';

export default {
    name: 'UpdatePassword',
    data: () => ({
        dialog: false,
        oldPassword: "",
        newPassword: "",
        repeatNewPassword: "",
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
        myError: "error",
      }),
    },
    methods: {
      async submit() {
        const success = await this.userStore.updatePassword(
          this.userID, this.oldPassword, this.newPassword
        );
        console.log("Success?: %s", success);
        if (success) {
          this.clearState();
        }
      },
      clearState() {
        this.oldPassword = "",
          this.newPassword = "";
          this.repeatNewPassword = "";
          this.dialog = false;
          this.userStore.clearError();
      },

      // logState() {
      //   console.log("Component error: %s", JSON.stringify(this.myError));
      //   console.log("Store error: %s", this.userStore.error);
      // }
      },
}

</script>