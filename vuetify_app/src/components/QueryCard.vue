<template>
  <v-container>
    <!-- <v-row justify="center"
      v-for="(value, i) in values"
      :key="i"
      > -->
      <!-- <v-col
        v-for="(variant, i) in variants"
        :key="i"
        cols="auto"
      > -->
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
                :items="menuItems"
                v-model="select"
                :key="selected"
                :selectable="selected"
                item-title="name"
                item-value="name"
                >
              </v-select>
                
              <!-- </div> -->
              <div class="text-paragraph">
                {{ select ? 
                        menuItems.filter((i) => i.name === select)[0].description 
                      : `Please select a ${title}`}}</div>
            </div>
          </v-card-item>

          <v-card-actions class="justify-center" v-if="select">
            <v-btn type="submit" @click.prevent="updateState()" :disabled="selected">
              {{ selected ? `${select} - Confirmed` : "Confirm Selection" }}
            </v-btn>
          </v-card-actions>
        </v-card>
      <!-- </v-col> -->
    <!-- </v-row> -->
  </v-container>
</template>

<script>

export default {
    props: {
      menuItems: Array,
      title: String,
      loggedIn: Boolean,
    },
    data() {
      return {
        select: "",
        selected: false,
      }
    },
    methods: {
      updateState() {
        if (!this.selected) {
        // console.log("Toggling my state!");
        this.$emit('clicked', this.select);
        this.selected = true;
      }
    },
    }
}
</script>
