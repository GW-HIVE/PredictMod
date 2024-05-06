<template>
  <v-container>
        <v-card
          class="mx-auto"
          max-width="1200"
        >
          <v-card-item>
            <div>
              <div class="text-overline mb-1">
                {{ title }}
              </div>
              <!-- <div class="text-h6 mb-1"> -->
              <v-select
                :disabled="confirmed"
                :items="menuItems"
                v-model="selection"
                
                :key="selection"
                :selectable="!confirmed"
                item-title="name"
                item-value="name"
                >
                <!-- defaultSelected="previousSelection" -->
              </v-select>
                
              <!-- </div> -->
              <div class="text-paragraph">
                {{ selection ? 
                        menuItems.filter((i) => i.name === selection)[0].description 
                      : `Please select a ${title}`}}</div>
            </div>
          </v-card-item>

          <v-card-actions class="justify-center" v-if="selection">
            <v-btn 
              type="submit" 
              @click.prevent="confirmState()" 
              :disabled="confirmed"
            >
              {{ confirmed ? `${selection} - Confirmed` : "Confirm Selection" }}
            </v-btn>
            <v-btn 
              type="submit" 
              @click.prevent="unconfirmState()" 
              :disabled="!confirmed"
            >
              Change selection
            </v-btn>
          </v-card-actions>
        </v-card>
      <!-- </v-col> -->
    <!-- </v-row> -->
  </v-container>
</template>

<script>
import { useQueryState } from '@/store/queryState';

export default {
    setup() {
      const queryState = useQueryState();
      return { queryState };
    },
    props: {
      menuItems: Array,
      title: String,
      loggedIn: Boolean,
      targetProp: String,
    },
    mounted() {
      this.getPreviousSelection();
    },
    data() {
      return {
        selection: "",
        confirmed: false,
      }
    },
    methods: {
      confirmState() {
          this.$emit('confirmed', this.targetProp, this.selection);
          // console.log("Confirmed: Selection is %s", this.selection);
          this.confirmed = true;
      },
      unconfirmState() {
        this.$emit('unconfirmed', this.targetProp);
        this.confirmed = false;
      },
      getPreviousSelection() {
        const currentState = this.queryState.getMenuSelection(this.targetProp);
        // console.log("---> Found current state: %s", currentState);
        if (currentState !== null) {
          this.selection = currentState;
          this.confirmed = true;
          return;
        }
        this.confirmed = false;
      },
    }
}
</script>
