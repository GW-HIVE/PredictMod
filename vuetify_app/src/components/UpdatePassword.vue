<template>
                <v-dialog 
                width="512"
                >
    <template v-slot:activator="{ props }">
                </template>
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Update Password</span>
                    </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col
                cols="6"
                sm="3"
                md="2"
              >
                <v-text-field
                  label="Old password*"
                  required
                ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                sm="3"
                md="2"
              >
                <v-text-field
                  label="New password"
                ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                sm="3"
                md="2"
              >
                <v-text-field
                  label="Retype new password"
                ></v-text-field>
              </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Save
                    </v-btn>
                </v-card-actions>
              </v-card>
    </v-dialog>
</template>

<script>

export default {
    name: 'UpdatePassword',
    data: () => ({
        dialog: true,
    })
}

</script>