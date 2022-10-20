<template>
<form @submit.prevent="sendFile" enctype="multipart/form-data">
    <div v-if="message"
        :class="`message ${error ? 'is-danger' : 'is-success'}`"
    >
        <div class="message-body">{{message}}</div>
    </div>
    
<div class="head"> 
    Choose a CSV of EHR data to analyze
    </div>

<div class="field">

<div class="file is-boxed is-primary">
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
    </label>
</div>

    </div>
    <div class="field">
        <button class="button is-info">Submit</button>
    </div>
</form>
</template>

<script>
import axios  from 'axios';
export default {
    name: "SimpleUploadEHR",
    data() {
        return {
            file: "",
            message: "",
            error: false
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
        }
    }
}


</script>