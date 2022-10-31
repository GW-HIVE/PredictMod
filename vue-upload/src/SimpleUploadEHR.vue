<template>

<form @submit.prevent="sendFile" enctype="multipart/form-data">

    
<div class="head font-weight-bold"> 
    Choose a CSV of EHR data to analyze
    </div>

<div class="field">

<div class="file is-boxed is-primary is-centered" v-if="message ==!'File has been uploaded'">
    <label class="file-label">
        
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
        <button class="button is-primary" v-if="message =='File has been uploaded'" @click="show = !show && getOutput">
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
        Based on the input EHR data, our algorithm predicts that KD would be {{EHRoutput}} in managing this patient's prediabetes
        </v-card-text>
    </div>
</form>


</template>

<script>

import axios  from 'axios';
export default {
    name: "SimpleUploadEHR",
    props: {

    },
    data() {
        return {
            file: "",
            message: "",
            image:[],
            show: false,
            error: false,
            EHRoutput:"SUCESSFUL"
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
                : "Only .csv files are allowed";
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
        async getOutput() {
            try {
                const response = await axios.get('/test');
                console.log(response.data);
                this.EHRoutput = response.data
                }
            catch(err) {
                this.message= err.response.data.error;
                this.error = true;
            }
        },
        
        revertFile() {
            this.message = ""
        }
    },
}


</script>