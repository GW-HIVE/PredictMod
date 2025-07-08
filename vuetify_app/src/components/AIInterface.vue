<template>

<!-- <button @click="count++">{{ modelName }}: Clicked {{ count }} times.</button> -->

<!-- <v-text-field label="AI-Generated summary">
    Larum ipsum dolor
</v-text-field> -->
  <!-- <v-btn color="primary" type="submit" @click.prevent="toggleQueryAI()">
    Query AI interface for more information?
  </v-btn> -->
<v-card flat>
    <v-card-title>AI-Generated overview</v-card-title>
    <v-container>
        <h1>Initial AI response</h1>
    <div 
        v-html="marked.parse(aiGenText.initial_response)"
        class="text-left"    
    >
    </div>
    </v-container>
    <v-container>
        <div v-for="response in aiGenText.parsed_topics">
            <h1>Additional queries...</h1>
            <div v-html="marked.parse(response)" class="text-left">
            </div>
        </div>
    </v-container>
    <v-container>
        <!-- <div v-for="response in aiGenText.parsed_topics"> -->
            <h1>Tertiary query results:</h1>
            {{ aiGenText.resource_results }}
        <!-- </div> -->
    </v-container>
    <!-- <v-container v-else>
        <VProgressCircular 
            indeterminate
            :width="5"
            :size="70">
        </VProgressCircular>
    </v-container> -->
</v-card>
<v-card >



</v-card>

</template>

<script setup>

import { onMounted, onUpdated, ref } from 'vue'
import { VProgressCircular } from 'vuetify/lib/components/index.mjs'
import { marked } from "marked"

const count = ref(0)

const aiGenResponse = ""
let queryAI = false

const toggleQueryAI = async () => {
    console.log("===> Querying AI <===")
    queryAI = !queryAI
    console.log("===> QueryAI is now: " + queryAI)
    await getAiResponse()
}

// const getAiResponse = async () => {

//     console.log("Running mode? " + process.env.NODE_ENV)
//     console.log("Vite values? " + import.meta.env.VITE_DEV_MIDDLEWARE_BASE)

//     let middlewareURL = process.env.NODE_ENV == "production" ?
//         import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE
//             :
//         import.meta.env.VITE_DEV_MIDDLEWARE_BASE
//     middlewareURL += "/api/query-ai/"

//     console.log("===> Querying endpoint at " + middlewareURL)

//     const middlewareResponse = await fetch(
//         middlewareURL
//     )
//     const responseContents = await middlewareResponse.json()
//     console.log("Got response: ", responseContents)

//     aiGenResponse.value = responseContents
//     console.log("===> New value?: " + JSON.stringify(aiGenResponse.value))
// }

defineProps([
    'modelName',
    "aiGenText"
])

</script>
