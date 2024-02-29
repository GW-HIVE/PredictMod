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
    <v-row justify="center"
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
          max-width="600"
        >
          <v-card-item>
            <div>
              <div class="text-overline mb-1">
                Analysis
              </div>
              <div class="text-h6 mb-1">
                {{ variant.name }}
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
    const variants = [
      {
        name: "'Omics",
        description: ""
      }, 
      {
        name: 'Metagenomics',
      },
      {
        name: 'EHR'
      },
      ]
</script>
