<template>
<v-banner
  single-line
  class="text-center"
  >
    <v-img
      src="../assets/MG_Model.jpg"
      id="intro-img"
      :height="400" 
      :cover="true"
      >
      <v-card-title class="text-center font-weight-bold text-bottom">
        <!-- 
            TODO: Get the text aligned, see e.g. here:
            https://stackoverflow.com/questions/56703740/how-to-bottom-align-button-in-card-irrespective-of-the-text-in-vuetify 
        -->
        Metagenomic Report
      </v-card-title>
      <v-card-text class="text-center">
        The gut microbiome consists of the genetic material of microbial communities found within the human gastrointestinal tract.
      </v-card-text>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

<v-col>
  <div class="text-center">
    <v-row>
        <v-select
          v-model="morbidityType"
          :items="morbidities"
          label="Select Disease Type">
        </v-select>
        <!-- TODO? We can change the button style as below -->
        <!-- <v-menu :selection="morbidities">
          <template v-slot:activator="{ props }">
            <v-btn
              color="primary"
              dark
              v-bind="props">
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(item, index) in items"
              :key="index"
            >
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu> -->
    </v-row>
    <v-row>
        <v-select
          v-model="interventionType"
          :items="interventions"
          label="Select Intervention">
        </v-select>
    </v-row>
    <v-row>
      <v-container>
        <v-card-title class="title text-center font-weight-bold" >
          Upload your data
        </v-card-title>
        <v-card-text class="text-center">
          <em>Make sure your file is in the PredictMod format</em>
        </v-card-text>
      </v-container>
      <v-container>
        <a href="../assets/w10003.png">
          <v-btn elevation="0" border @click.prevent="downloadItem(item)">
              File Download (Not Working!)
          </v-btn>
        </a>
      </v-container>
    </v-row>
    <v-row>
        <!-- 
            TODO
            See here for a good example of making the Vue button trigger an
            upload method, rather than relying on Vuetify's internal 
            upload fields
            https://ourcodeworld.com/articles/read/1424/how-to-use-a-button-as-a-file-uploader-with-vuetify-in-vuejs
         -->
          <FileUpload :upload-target-u-r-l="myTargetURL" />

         <!-- Dead code below...? -->
        <!-- <v-file-input
          label="Upload Sample Data"
          variant="outlined"
          >
        </v-file-input> -->
    </v-row>
  </div>
</v-col>

</template>

<script>
import axios  from 'axios';
import GetMGoutput from './GetMGoutput.vue'
import FileUpload from '../components/FileUpload.vue'

export default {
    name: "SimpleUploadMG",
    components: { GetMGoutput, FileUpload },
    props: {
        
    },
    data() {
        return {
            file: "",
            message: "",
            error: false,
            show: false,
            morbidities: [
                "Prediabetes",
            ],
            morbidityType: "Prediabetes",
            interventions: [
                "Lifestyle Change",
            ],
            interventionType: "Lifestyle Change",
            myTargetURL: "mg",
        }
    },
    // This is useful to keep around in case we start needing to pass state around
    // async created() {
    //     const labelURL = () => new Promise((resolve, reject) => {
    //         setTimeout(() => {
    //           resolve("mg");
    //         }, 50);
    //     });
    //     this.myTargetURL = await labelURL();
    // },

    methods: {
        // selectFile() {
        //     const file = this.$refs.MG.files[0];
        //     const allowedTypes = ["text/csv","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"];
        //     const MAX_SIZE = 200000;
        //     const tooLarge = file.size > MAX_SIZE;

        //     if(allowedTypes.includes(file.type) && !tooLarge) {
        //         this.file = file;
        //         this.error = false;
        //         this.message = "";
        //     } else {
        //         this.error = true;
        //         this.message = tooLarge 
        //         ? `Too large. Max size is ${MAX_SIZE/1000}kb` 
        //         : "Only .csv, .xls, and .xlsx files are allowed";
        //     }
        // },

        downloadItem () {
            // Depending on how we proceed, see here for download support:
            // https://stackoverflow.com/questions/53772331/vue-html-js-how-to-download-a-file-to-browser-using-the-download-tag
            //
            console.log("---> File download is not yet supported");
        },

        // async sendFile() {
            
        //   console.log("---> Sending file!");          
          
        //   const formData = new FormData();
        //   formData.append('MG', this.file);

        //     // try {
        //     //     await axios.post('/upload-MG', formData);
        //     //     this.message = "File has been uploaded";
        //     //     this.file = ""
        //     //     this.error = false
        //     // }   catch(err) {
        //     //     this.message = err.response.data.error;
        //     //     this.error = true;
        //     // }
        // },
        // revertFile() {
        //     this.message = ""
        // }
    }
}


</script>