<template>
<v-container fluid>
    <v-row>
        <v-col v-if="props.metadata.confusion_matrix">
            <v-img :src="'data:image/png;base64,'+props.metadata.confusion_matrix" v-if="!props.metadata.feature_importance" width="50%">
            </v-img>
            <v-img :src="'data:image/png;base64,'+props.metadata.confusion_matrix" v-if="props.metadata.feature_importance" width="100%">
            </v-img>
        </v-col>
        <v-col v-if="props.metadata.feature_importance">
          <v-container style="text-align: left">
            <b>Top feature importances</b>
            <div justify="left">
            <li v-for="feature in props.metadata.feature_importance.slice(0,10)">
                {{ feature[0] }}: <b>{{ parseFloat(feature[1]).toFixed(4) }}</b>
            </li>
            </div>
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