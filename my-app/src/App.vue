<template>
  <vue-csv-import
      v-model="csv"
      :fields="{name: {required: false, label: 'Organism'}, age: {required: true, label: 'Relative Abundance'}}"
  >
      <vue-csv-toggle-headers></vue-csv-toggle-headers>
      <vue-csv-errors></vue-csv-errors>
      <vue-csv-input name="file"></vue-csv-input>
      <vue-csv-map></vue-csv-map>
  </vue-csv-import>
  <button @click="VueCsvImport">
    Press me
  </button>
</template>

<script>
import {VueCsvImport} from 'vue-csv-import';

export default {
  components: VueCsvImport
}

</script>