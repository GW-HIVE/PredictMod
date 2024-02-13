<!-- <template>
    <v-container>
      <v-row align="center" justify="center">
        <v-col
          v-for="(variant, i) in variants"
          :key="i"
          cols="auto"
        >
          <v-card
            class="mx-auto"
            max-width="344"
            :variant="variant"
          >
            <v-card-item>
              <div>
                <div class="text-overline mb-1">
                  {{ variant }}
                </div>
                <div class="text-h6 mb-1">
                  Headline
                </div>
                <div class="text-caption">Greyhound divisely hello coldly fonwderfully</div>
              </div>
            </v-card-item>
  
            <v-card-actions>
              <v-btn>
                Button
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template> -->

<!-- <script setup>
    const variants = ['elevated', 'flat', 'tonal', 'outlined']
</script> -->

<template>
  <v-container>
    <v-row align="left" justify="center"
      v-for="(variant, i) in variants"
      :key="i"
      >
      <!-- <v-col
        v-for="(variant, i) in variants"
        :key="i"
        cols="auto"
      > -->
        <v-card
          class="mx-auto"
          max-width="344"
          :variant="variant"
        >
          <v-card-item>
            <div>
              <div class="text-overline mb-1">
                {{ variant }}
              </div>
              <div class="text-h6 mb-1">
                Headline
              </div>
              <div class="text-caption">Greyhound divisely hello coldly fonwderfully</div>
            </div>
          </v-card-item>

          <v-card-actions>
            <v-btn>
              Button
            </v-btn>
          </v-card-actions>
        </v-card>
      <!-- </v-col> -->
    </v-row>
  </v-container>
</template>

<script setup>
    const variants = ['Step 1', 'Step 2', 'Step 3']
</script>
