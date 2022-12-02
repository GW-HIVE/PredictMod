<template>

<form @submit.prevent="sendFile" enctype="multipart/form-data">


<div class="head font-weight-bold"> 
    Analyze Metagenomic data
    </div>

<div class="field">

<div class="file is-boxed is-primary is-centered" v-if="message == !'File has been uploaded'">
    <label class="file-label">
        
        <input 
        type="file"
        ref="MG"
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
        <button class="button is-info is-centered" v-if="message ==!'File has been uploaded'">Submit</button>
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
            <GetMGoutput/>
        </v-card-text>
        <v-btn elevation="0" border>
          <v-list-item href="http://localhost:3344/example-MG"> Example data </v-list-item>
        </v-btn>
    </div>
</form>
</template>

<script>
import axios  from 'axios';
import GetMGoutput from './GetMGoutput.vue'
export default {
    name: "SimpleUploadMG",
    components: {GetMGoutput},
    props: {
        
    },
    data() {
        return {
            file: "",
            message: "",
            error: false,
            show: false
        }
    },

    methods: {
        selectFile() {
            const file = this.$refs.MG.files[0];
            const allowedTypes = ["text/csv","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"];
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

        async sendFile() {
            const formData = new FormData();
            formData.append('MG', this.file);
            
            try {
                await axios.post('/upload-MG', formData);
                this.message = "File has been uploaded";
                this.file = ""
                this.error = false
            }   catch(err) {
                this.message = err.response.data.error;
                this.error = true;
            }
        },
        revertFile() {
            this.message = ""
        }
    }
}


</script>