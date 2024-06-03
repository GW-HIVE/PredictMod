<template>

<v-autocomplete
  :items="results"
  v-model="selection"
  prepend-inner-icon="mdi-magnify"
  style="max-width: 350px;"
  menu-icon=""
  item-title="name"
  density="comfortable"
  placeholder="Search PredictMod"
  @input="filterResults"
  @keyup.enter="submitSelection"
>
  <!-- item-value="link" -->
<!-- @click.prevent="updateSelection" -->
  <!-- autocomplete="off" -->
</v-autocomplete>

</template>

<script>

import countries from '@/assets/countries.json'

import { useAppStore } from '@/store/app';

export default {
  name: 'SearchAutocomplete',
  setup() {
    const appStore = useAppStore();
    return { appStore }
  },
  props: {
    items: {
      type: Array,
      required: false,
      default: () => countries,
    },
    isAsync: {
      type: Boolean,
      required: false,
      default: false,
    },
    // watch: {
    // items: function (value, oldValue) {
    //   console.log("Replaced %s with %s", oldValue, value);
    //   if (this.isAsync) {
    //     this.results = value;
    //     this.isOpen = true;
    //     this.isLoading = false;
    //   }
    // }
    // selection: function (newSelection, oldSelection) {
    //   console.log("...New: ", newSelection);
    //   console.log("...Old: ", oldSelection);
  //   }
  // },
  },
  data() {
    return {
      // search: '',
      results: [],
      isOpen: false,
      arrowCounter: -1,
      selection: [],
      // items: this.appStore.modelInitialSearch,
    };
  },
  methods: {
    filterResults(event) {
      const search = event.data;
      // TODO: Search on alphanumerics works as expected, but not on backspace, etc.
      if (search) {
        console.log("Filtering results over %s", search);
        this.results = this.items.filter(
          item => item.name.toLowerCase().indexOf(search.toLowerCase()) > -1)
        .map(item => item.name);
    } else {
      return this.results = this.items;
    }
    },
    // updateSelection() {
    //   console.log("Executing query");
    //   // console.log("Results: %s", this.results);
    //   // console.log("Items: %s", this.items);
    //   console.log("Selection is ", this.selection);
    // },
    submitSelection() {
      const item = this.items.filter((i) => i.name === this.selection)[0];
      this.results = this.items;
      this.selection = [],
      this.$router.push(item.link);
    },

  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  destroyed() {
    document.removeEventListener('click', this.handleClickOutside);
  }
};
</script>