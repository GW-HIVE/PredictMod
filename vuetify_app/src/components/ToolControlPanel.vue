<template>
<v-col cols="11">
<v-row class="justify-center">
<v-btn type="submit" @click="alertTBD(source=`Review`)">
    Review Available Models
</v-btn>
<router-link :to="queryState.modelAnchor">
    <v-btn>
        Learn More
    </v-btn>
</router-link>
    <FileDownload :download-target-u-r-l="queryState.targetURL" />
</v-row>
</v-col>
<v-col cols="11">
<v-row class="justify-center pa-2" v-if="loggedIn">
    <FileUpload :upload-target-u-r-l="queryState.targetURL" />
</v-row>
</v-col>
<v-col cols="11">
<v-row class="justify-center pa-8" v-if="!loggedIn">
    <v-btn color="primary" type="submit" @click.prevent="alertTBD(source=`Default submission`)">
        Example Analysis
    </v-btn>
</v-row>
</v-col>
<!-- 
    <v-row>
    <v-btn color="primary" @click="alertTBD(source=`Analysis`)">
        {{ loggedIn ? "Launch Analysis" : "See output from example file" }}
    </v-btn>
</v-row>
-->
</template>

<script>
import { useUserStore } from '@/store/user';
import { useQueryState } from '@/store/queryState';
import FileDownload from '@/components/FileDownload.vue';
import FileUpload from '@/components/FileUpload.vue';

export default {

    name: 'ToolControlPanel',
    setup() {
        const userStore = useUserStore();
        const queryState = useQueryState();
        return { userStore, queryState };
    },
    computed: {
        loggedIn: function() {
            console.log("User store has value %s", this.userStore.user);
            return this.userStore.user ? true : false
        },
    },
    // props: {
        // selections: Object,
        // targetURL: String,
        // modelAnchor: String,
    // },
    methods: {
        alertTBD(source) {
            alert(source + " functionality is under construction");
        },
    },
    components: { FileDownload, FileUpload },


}
</script>