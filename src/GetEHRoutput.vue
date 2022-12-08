<template>
    <v-card-text>Prediction: {{EHRoutput}}</v-card-text>

  </template>
  
  <script>
  export default {
    name: "get-request",
    data() {
      return {
        EHRoutput: null
      };
    },
    async created() {
      // Simple GET request using fetch
      await fetch("/output-EHR")
        .then(response => response.json())
        .then(data => (this.EHRoutput = data.title));
    }
  };
  </script>
  