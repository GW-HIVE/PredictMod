<template>
<form @submit.prevent="sendFile" enctype="multipart/form-data">
    <div class="field">
        
        <div class="file is-boxed is-primary">
            <label class="file-label">
                
                <input 
                type="file"
                ref="file"
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
        <button class="button is-info">Send</button>
    </div>
</form>
</template>

<script>
import axios  from 'axios';
export default {
    name: "SimpleUpload",
    data() {
        return {
            file: ""
        }
    },

    methods: {
        selectFile() {
            this.file = this.$refs.file.files[0];
        },

        async sendFile() {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                await axios.post('/upload', formData);
            }   catch(err) {
                console.log(err);
            }
        }
    }
}


</script>