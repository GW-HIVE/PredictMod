<template>

<!--this component was adapted from a Youtube tutorial. 
    For more information, see parts 1-3 of the following series: 
    https://www.youtube.com/watch?v=GXe_JpBQLTQ -->
<form @submit.prevent="sendFile" enctype="multipart/form-data">

    
<!-- header for component --> 
<div class="head font-weight-bold"> 
    Analyze EHR data
</div>

<div class="field">

<!-- if file has not been uploaded, allow user to select and upload file-->
<div class="file is-boxed is-primary is-centered" v-if="message ==!'File has been uploaded'">
    <label class="file-label">
        
        <!--when clicked, allow user to select file. Use REF "EHR" for file from now on. This will be important on server side-->
        <input 
        type="file"
        ref="EHR"
        @change="selectFile"
        class="file-input"
        />

        <span class="file-cta">
            <span class="file-icon">
                <i class="fas fa-upload"></i>
            </span>
            <div class="span file-label">
                Choose a file...
            </div>
        </span>

        <span v-if="file" class="file-name">{{file.name}}</span>
        <div v-if="message"
        :class="`message ${error ? 'is-danger' : 'is-success'}`"
        >
        
        <div class="message-body">{{message}}</div>
        </div>
    </label>
</div>

    </div>
    <div class="field"> 
        <button class="button is-info is-centered" v-if="message == !'File has been uploaded'">Submit</button>
        
    </div>
    <div class="field">
        <button class="button is-primary" v-if="message =='File has been uploaded'" @click="show = !show">
        Show Results
        </button>
    </div>
    <div class="field">
        <button class="button is-info" v-if="message =='File has been uploaded'" @click="revertFile">
        Upload a different file
        </button>
    </div>
    <div class="field">
        <v-card-text class="text-left" v-if="show && message=='File has been uploaded'">
         <GetEHRoutput/>
        </v-card-text>
        <v-btn elevation="0" border>
          <v-list-item href="http://localhost:3344/example-EHR"> Example data </v-list-item>
        </v-btn>
    </div>
</form>


</template>

<script>

import axios  from 'axios';
import GetEHRoutput from './GetEHRoutput.vue'
export default {
    name: "SimpleUploadEHR",
    components: {GetEHRoutput},
    props: {

    },
    data() {
        return {
            file: "",
            message: "",
            image:[],
            show: false,
            error: false,
        }
    },

    methods: {

        //method to select file, with allowedTypes restricting filetypes and size before being sent to server
        selectFile() {
            const file = this.$refs.EHR.files[0];
            //allowed filetypes can be changed by adding/removing mimetypes to allowedTypes
            const allowedTypes = ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel" ];
            //can alter max filesize allowed (in b) by changing value MAX_SIZE
            const MAX_SIZE = 200000;
            const tooLarge = file.size > MAX_SIZE;

            if(allowedTypes.includes(file.type) && !tooLarge) {
                this.file = file;
                this.error = false;
                this.message = "";
            } else {
                this.error = true;
                this.message = tooLarge 
                ? `Too large. Max size is ${MAX_SIZE/1000}kb` 
                : "Only .csv, .xls, and .xlsx files are allowed";
            }
        },
        //will send file to server if no errors come up
        async sendFile() {
            const formData = new FormData();
            formData.append('EHR', this.file);

            try {
                await axios.post('/upload-EHR', formData);
                this.message = "File has been uploaded";
                this.file = ""
                this.error = false
            }   catch(err) {
                this.message = err.response.data.error;
                this.error = true;
            }
        },
        async created () {
            // Simple GET request using fetch
            fetch("/output")
                .then(response => response.json())
                .then(data => (this.EHRoutput = data.title));
        },
        
        revertFile() {
            this.message = ""
        }
    },
}


</script>