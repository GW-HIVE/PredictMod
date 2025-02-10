<template>
  <v-col>
  <v-row v-for="obj in data">
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
        href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" 
        target="_blank"
      >
        <v-icon>mdi-help-box</v-icon>
      </v-btn>
      <v-icon icon="mdi-help mdi-spin"></v-icon>
    </v-toolbar>
  <v-card-title>
    <!-- {{ obj.Method }} -->
      <!-- <a :href=modelsURL+obj.fields.link>{{ obj.fields.name }}</a> -->
  </v-card-title>
  <!-- <v-icon ></v-icon> -->
  <v-card-text>
      <!-- {{ obj['Confusion Matrix'] ? "Confusion Matrix" + obj['Confusion Matrix'] : null }}<br> -->
      <v-img 
        v-if="obj['Confusion Matrix']"
        :src="'data:image/png; base64, ' + obj['Confusion Matrix']"
        :height="300"
        :width="800"
      >
      </v-img>
      <v-img
        v-if="obj.image"
        :src="'data:image/png; base64, ' + obj.image"
        :height="300"
        :width="800"
      ></v-img>
      
      {{ obj['Explained Variance'] ? "Explained Variance: " + JSON.stringify(obj['Explained Variance']) : null }}<br>
      {{ obj.Accuracy ? "Accuracy: " + obj.Accuracy*100 + "%" : null }}<br>
  </v-card-text>
  </v-card>
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
