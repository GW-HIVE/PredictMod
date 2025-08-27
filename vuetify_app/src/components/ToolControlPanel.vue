<template>
<v-container v-if="!modelView">
  <h4>Current Model: {{ queryState.targetURL.name }}</h4>
</v-container>
<v-col cols="11">
<v-row class="justify-center">
<!-- <v-btn type="submit" @click="alertTBD(source=`Review`)"> -->
<v-btn ref="button" v-if="!modelView">
    Review Available Models
</v-btn>
<!-- See https://stackoverflow.com/a/76930390 -->
<v-select
  :items="queryState.targetURLs"
  item-title="name"
  item-value="link"
  hide-details
  return-object
  v-model="queryState.targetURL"
  :menu-props="{activator: button, openOnClick: true}"
  v-show="false"
>
  <!-- v-model="selectedModel" -->
</v-select>
<router-link :to="'models/' + queryState.targetURL.link" v-if="!modelView">
    <v-btn>
        Learn More About The Model
    </v-btn>
</router-link>
    <!-- <FileDownload :download-target-u-r-l="queryState.targetURL" /> -->
    <v-btn color="primary" small @click.prevent="downloadPreview">
            Download example data file
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
    </v-btn>
</v-row>

</v-col>
<v-col cols="11" v-if="loggedIn">
<v-row class="justify-center pa-2">
    <FileUpload :upload-target-u-r-l="modelView ? modelName : `${queryState.targetURL.link}`" />
</v-row>
</v-col>
<v-col cols="11" v-if="!loggedIn">
<v-row class="justify-center pa-8">
  <FileUpload :upload-target-u-r-l="modelView ? modelName : `${queryState.targetURL.link}`" />
</v-row>
</v-col>
</template>

<script setup>
import { computed, ref } from 'vue';

import { useUserStore } from '@/store/user';
import { useQueryState } from '@/store/queryState';
// import FileDownload from '@/components/FileDownload.vue';
import DownloadService from '@/services/DownloadService';
import FileUpload from '@/components/FileUpload.vue';

const button = ref()
// const selectedModel = ref()

const userStore = useUserStore()
const queryState = useQueryState()

const props = defineProps({
  targetURL: {type: String},
  modelName: {type: String},
  modelView: {type: Boolean, default: false},
})

function alertTBD(source) {
    alert(source + " functionality is under construction");
}

async function downloadPreview() {
    const targetName = props.modelName ? props.modelName : queryState.targetURL.link;
    // console.log("TCP: Downloading from target ", targetName);
    const response = await DownloadService.download(targetName, () => {
    });
    // console.log("TCP: Collected data:\n%s", response);
    if (response.error) {
        console.log("Download experienced an error: ", response.error);
        alert("Download experienced an error: " + response.error);
    } else {
    queryState.filePreviewData = response;
    queryState.downloadDrawer = true;
    }
}

const loggedIn = computed(() => {
  return userStore.user ? true : false
})

</script>
