<template>
<v-container fluid>
    <v-row>
        <v-col v-if="props.metadata.confusion_matrix">
            <v-img :src="'data:image/png;base64,'+props.metadata.confusion_matrix" width="100%">
            </v-img>
        </v-col>
        <v-col v-if="props.metadata.feature_importance">
          <v-container style="text-align: left">
            <b>Top feature imporatances</b>
            <li v-for="feature in props.metadata.feature_importance.slice(0,10)">
                <div justify="left">{{ feature[0] }}: <b>{{ parseFloat(feature[1]).toFixed(4) }}</b></div>
            </li>
            </v-container>
        </v-col>
    </v-row>
</v-container>
</template>

<script setup>
// import { reactive, computed } from 'vue'

const props = defineProps(['metadata'])
// console.log("---> Dashboard mounting <---")
// console.log("Props were " + JSON.stringify(props))

// const formattedFeatures = computed(() => {

// })

</script>