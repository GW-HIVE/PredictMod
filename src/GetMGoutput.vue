<template>
    <v-card-text>Prediction: {{MGoutput}}</v-card-text>

  </template>
  
  <script>
  export default {
    name: "get-request",
    data() {
      return {
        MGoutput: null
      };
    },
    async created() {
      // Simple GET request using fetch
      await fetch("/output-MG")
        .then(response => response.json())
        .then(data => (this.MGoutput = data.title));
    }
  };
  </script>
  