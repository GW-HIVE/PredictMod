<template>
<v-col cols="11">
<v-row class="justify-center">
<!-- <v-btn type="submit" @click="alertTBD(source=`Review`)"> -->
<v-btn ref="button">
    Review Available Models
</v-btn>
<v-select
  :items="queryState.targetURLs"
  item-title="name"
  item-value="link"
  return-object
  hide-details
  :menu-props="{activator: button, openOnClick: true}"
  v-show="false"
>
</v-select>
<router-link :to="'models/' + queryState.targetURL" v-if="!targetURL">
    <v-btn>
        Learn More About This Model
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
    <FileUpload :upload-target-u-r-l="targetURL ? modelName : `${queryState.targetURL}`" />
</v-row>
</v-col>
<v-col cols="11" v-if="!loggedIn">
<v-row class="justify-center pa-8">
    <v-btn color="primary" type="submit" @click.prevent="alertTBD(source=`Default submission`)">
        Example Analysis
    </v-btn>
</v-row>
</v-col>
<v-btn @click.prevent="showQueryState()">
    Show state?
</v-btn>
<!-- 
    <v-row>
    <v-btn color="primary" @click="alertTBD(source=`Analysis`)">
        {{ loggedIn ? "Launch Analysis" : "See output from example file" }}
    </v-btn>
</v-row>
-->
</template>

<script setup>
import { computed, ref } from 'vue';

import { useUserStore } from '@/store/user';
import { useQueryState } from '@/store/queryState';
// import FileDownload from '@/components/FileDownload.vue';
import DownloadService from '@/services/DownloadService';
import FileUpload from '@/components/FileUpload.vue';

const button = ref()

const userStore = useUserStore()
const queryState = useQueryState()

const props = defineProps({
  targetURL: {type: String},
  modelName: {type: String},
})

function alertTBD(source) {
    alert(source + " functionality is under construction");
}
function showQueryState() {
    console.log("===> Present query state 'model anchor': " + this.queryState.modelAnchor)
    console.log("===> Present query state 'targetURL': " + this.queryState.targetURL)
}
function toggleMenu() {
  this.showMenu = !this.showMenu;
  console.log("Show menu is now: " + this.showMenu)
}
async function downloadPreview() {
    const targetName = this.modelName ? this.modelName : this.queryState.targetURL;
    // console.log("TCP: Downloading from target ", targetName);
    const response = await DownloadService.download(targetName, () => {
    });
    // console.log("TCP: Collected data:\n%s", response);
    if (response.error) {
        console.log("Download experienced an error: ", response.error);
        alert("Download experienced an error: " + response.error);
    } else {
    this.queryState.filePreviewData = response;
    this.queryState.downloadDrawer = true;
    }
}

const loggedIn = computed(() => {
  return userStore.user ? true : false
})

</script>
