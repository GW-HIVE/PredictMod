<template>

<!-- <button @click="count++">{{ modelName }}: Clicked {{ count }} times.</button> -->

<!-- <v-text-field label="AI-Generated summary">
    Larum ipsum dolor
</v-text-field> -->

<v-card flat>
    <v-card-title>AI-Generated overview</v-card-title>
    <v-container v-if="aiGenResponse">
        "Got a response!"
    </v-container>
    <v-container v-else>
        <VProgressCircular 
            indeterminate
            :width="5"
            :size="70">
        </VProgressCircular>
    </v-container>
</v-card>
<v-card >



</v-card>

</template>

<script setup>

import { ref } from 'vue'
import { VProgressCircular } from 'vuetify/lib/components/index.mjs'
const count = ref(0)

const aiGenResponse = null

const getAiResponse = async () => {
    
}

defineProps([
    'modelName'
])

</script>
