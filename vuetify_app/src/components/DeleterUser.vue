<template>
      <v-btn @click="dialog = true">
        Delete User?
      </v-btn>
          <v-dialog width="512" v-model="dialog">
                <v-card>
                    <v-card-title>
                        <span class="text-h3">Delete User?</span>
                    </v-card-title>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="clearState()"
          >
            Cancel
          </v-btn>
          <v-btn
            color="red-darken-1"
            variant="text"
            @click="submit()"
          >
            Confirm
                    </v-btn>
              </v-card>
    </v-dialog>
</template>

<script>
import { mapWritableState } from 'pinia';
import { useUserStore } from '@/store/user';

export default {
    name: 'DeleteUser',
    data: () => ({
        dialog: false,
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
        console.log("Deleting user %s", this.userID);
        const success = await this.userStore.deleteUser(this.userID);
        console.log("Deletion operation: Reported success %s", success);
        if (success) {
          this.clearState();
        } else {
          this.clearState();
        }
      },
      clearState() {
        this.userStore.clearError();
        this.dialog = false;
      },

  },
}

</script>