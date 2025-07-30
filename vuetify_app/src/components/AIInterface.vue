<template>

<!-- <button @click="count++">{{ modelName }}: Clicked {{ count }} times.</button> -->

  <!-- <v-btn color="primary" type="submit" @click.prevent="toggleQueryAI()">
    Query AI interface for more information?
  </v-btn> -->

<v-card outlined>
    <v-card-title>AI Chat Assistant</v-card-title>
    
    <v-card v-for="response in aiGenResponses"
        v-html="response"
        class="text-left"    
    >
</v-card>
</v-card>
    <v-text-field
        label="Enter query for AI assistant"
        v-model="currentInput" 
        @input="logEvent()"
    >
    </v-text-field>
<v-btn color="primary" type="submit" @click.prevent="queryAI()">
    Query AI interface for more information?
</v-btn>

</template>

<script>
import { marked } from "marked";

export default {
  data() {
    return {
      nextInput: '',
      aiGenResponses: [],
      currentInput: ''
    }
  },
  mounted() {
    this.getAiResponse();
  },
  methods: {
    logEvent() {
      console.log(this.currentInput);
    },
    queryAI() {
      console.log("===> Querying AI <===");
      console.log("Current Input is " + this.currentInput);
      this.getAiResponse(this.currentInput)
    },
    getAiResponse(queryText) {
      console.log("Running mode? " + process.env.NODE_ENV);
      console.log("Vite values? " + import.meta.env.VITE_DEV_MIDDLEWARE_BASE);

      let middlewareURL = (process.env.NODE_ENV === 'production') ?
        import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE :
        import.meta.env.VITE_DEV_MIDDLEWARE_BASE;

      if (!queryText) {
        queryText = this.initialQuery;
      }
      middlewareURL += `/api/query-ai/?q=${queryText}`;

      console.log("===> Querying endpoint at " + middlewareURL);

      fetch(middlewareURL)
        .then(response => response.json())
        .then(data => {
          this.aiGenResponses.push(marked.parse(data.response));
        });
    }
  },
  props: [
    'modelName',
    'initialQuery']
    ,
  env: {
    NODE_ENV: process.env.NODE_ENV,
    VITE_DEV_MIDDLEWARE_BASE: import.meta.env.VITE_DEV_MIDDLEWARE_BASE,
    VITE_DOCKER_MIDDLEWARE_BASE: import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE
  }
}
</script>

<!-- 
 Composition API appears to break the v-text-field in Vuetify,
 reverting to Options API. NB: Sourced directly from a Llama3.2 query 
 to "convert this script"...
 -->
<!-- <script setup>

import { onMounted, onUpdated, ref, reactive } from 'vue'
import { VProgressCircular } from 'vuetify/lib/components/index.mjs'
import { marked } from "marked"

const nextInput = ref("")
const aiGenResponses = reactive([])

let currentInput = ref("")

let queryAI = false

const logEvent = () => {
    console.log(currentInput.value)
}

onMounted(() => {
    getAiResponse()
})

const toggleQueryAI = async () => {
    console.log("===> Querying AI <===")
    queryAI = !queryAI
    console.log("===> QueryAI is now: " + queryAI)
    console.log("Current Input is " + currentInput.value)
    await getAiResponse(currentInput.value)
    currentInput = ""
}

const getAiResponse = async (queryText = null) => {

    console.log("Running mode? " + process.env.NODE_ENV)
    console.log("Vite values? " + import.meta.env.VITE_DEV_MIDDLEWARE_BASE)

    let middlewareURL = process.env.NODE_ENV == "production" ?
        import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE
            :
        import.meta.env.VITE_DEV_MIDDLEWARE_BASE
    const query = queryText == null ? props.initialQuery : queryText
    middlewareURL += `/api/query-ai/?q=${query}`

    console.log("===> Querying endpoint at " + middlewareURL)

    const middlewareResponse = await fetch(
        middlewareURL
    )
    const responseContents = await middlewareResponse.json()
    // console.log("Got response: ", responseContents)

    aiGenResponses.push(responseContents.response)
    // console.log("===> New value?: " + JSON.stringify(aiGenResponses))
}

const props = defineProps([
    'modelName',
    'initialQuery',
])

</script> -->
