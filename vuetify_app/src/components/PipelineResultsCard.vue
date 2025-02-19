<template>
  <v-col>
  <v-row v-for="obj in data">
    <v-container fluid>
    <v-card 
      variant="flat"
      class="text-left"
      >
      <!-- append-icon="mdi-help-box" -->
      <v-toolbar density="compact">
        {{  obj.Method }}
        <v-spacer></v-spacer>
      <v-btn 
        icon 
        :href="obj['Help URL']"
        target="_blank"
      >
        <v-icon>mdi-help-box</v-icon>
      </v-btn>
      <!-- 
      Fun, spinning icon but no practical use for this here yet....
      <v-icon icon="mdi-help mdi-spin"></v-icon> 
      -->
    </v-toolbar>
  <v-card-title>
    <!-- {{ obj.Method }} -->
      <!-- <a :href=modelsURL+obj.fields.link>{{ obj.fields.name }}</a> -->
  </v-card-title>
  <!-- <v-icon ></v-icon> -->
  <v-card-text>
      <!-- {{ obj['Confusion Matrix'] ? "Confusion Matrix" + obj['Confusion Matrix'] : null }}<br> -->
    <v-container v-if="obj['Confusion Matrix']">
      <!-- v-if="obj['Confusion Matrix']" -->
       Confusion Matrix - From Training Set
      <v-img
        title="From model training"
        :src="'data:image/png; base64, ' + obj['Confusion Matrix']"
        :height="400"
        :width="800"
      >
      </v-img>
    </v-container>
      <v-img
        v-if="obj.image && obj.image !== 'TBD'"
        :src="'data:image/png; base64, ' + obj.image"
        :height="400"
        :width="800"
      ></v-img>
      <!-- NB: See S/O for notes on rendering HTML (to avoid empty lines with the `<br>` tags) - https://stackoverflow.com/a/56882737 -->
      {{ obj['Explained Variance'] ? "Explained Variance: " + JSON.stringify(obj['Explained Variance']) : null }}<br>
      {{ obj.Accuracy ? "Accuracy: " + obj.Accuracy*100 + "%" : null }}<br>
      {{ obj.Prediction ? "Model Prediction: " + obj.Prediction: null }}<br>

  </v-card-text>
  </v-card>
</v-container>
</v-row>
</v-col>
</template>

<script>

// const modelsURL = '/predictmod/models/'
// const modelsURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/models/': "/predictmod/models/";

export default {
  name: "PipelineResults",
  props: {
      data: Object,
  },
  data() {
      return {
      }
  },
  mounted() {
  },
  methods: {
      routeTo(newLocation) {
        this.$router.push(newLocation);
      }
  }
}

</script>
