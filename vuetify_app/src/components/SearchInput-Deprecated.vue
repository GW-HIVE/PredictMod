<!-- 
    Credit to https://stevencotterill.com/articles/how-to-build-an-autocomplete-field-with-vue-3
    and code here: https://github.com/stevie-c91/vue-3-autocomplete/blob/master/src/App.vue
    (No license listed but it was introduced as a tutorial)
 -->

<template>
    <div class="bg-gray-50 min-w-screen min-h-screen justify-center items-center">
      <div class="max-w-xs relative space-y-3">
        <!-- <label
          for="search"
          class="text-gray-900"
        >
          Type to see details from available models
        </label>
   -->
        <input
          type="text"
          id="search"
          autocomplete="off"
          v-model="searchTerm"
          placeholder="Search..."
          class="p-3 mb-0.5 w-full border border-gray-300 rounded"
          position="fixed"
        >
  
        <ul
          v-if="searchCountries.length"
          class="w-full rounded bg-white border border-gray-300 px-4 py-2 space-y-1 relative z-10"
        >
          <ul class="px-1 pt-1 pb-2 font-bold border-b border-gray-200 relative z-10">
            Showing {{ searchCountries.length }} of {{ countries.length }} results
          </ul>
          <li
              v-for="country in searchCountries"
              :key="country.name"
              @click="selectCountry(country.name)"
              class="cursor-pointer hover:bg-gray-100 p-1"
          >
            {{ country.name }}
          </li>
        </ul>
  
        <p
          v-if="selectedCountry"
          class="text-lg pt-2 absolute"
        >
          You have selected: <span class="font-semibold">{{ selectedCountry }}</span>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import countries from '@/assets/countries.json'
  import {ref, computed} from 'vue'
  
  export default {
    setup() {
      let searchTerm = ref('')
  
      const searchCountries = computed(() => {
        if (searchTerm.value === '') {
          return []
        }
  
        let matches = 0
  
        return countries.filter(country => {
          if (country.name.toLowerCase().includes(searchTerm.value.toLowerCase()) && matches < 10) {
            matches++
            return country
          }
        })
      });
  
      const selectCountry = (country) => {
        selectedCountry.value = country
        searchTerm.value = ''
      }
  
      let selectedCountry = ref('')
  
      return {
        countries,
        searchTerm,
        searchCountries,
        selectCountry,
        selectedCountry
      }
    }
  }
  </script>