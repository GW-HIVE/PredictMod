<template>

<v-banner
  single-line
  class="text-center"
  >
    <v-img
      src="../assets/EHR_Model.jpg"
      id="intro-img"
      :height="400" 
      :cover="true"
      >
      <v-card-title class="text-center font-weight-bold text-bottom">
        <!-- 
            TODO: Get the text aligned, see e.g. here:
            https://stackoverflow.com/questions/56703740/how-to-bottom-align-button-in-card-irrespective-of-the-text-in-vuetify 
        -->
        Electronic Health Record Report
      </v-card-title>
      <v-card-text class="text-center">
        Electronic Health Records (EHR) contain patient-centered clinical records obtained through regular 
        medical checkups.

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
        <a>
          <v-btn elevation="0" border @click.prevent="downloadItem(item)">
              File Download
          </v-btn>
        </a>
      </v-container>
    </v-row>
    <v-container>
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
  </v-container>
  </div>
</v-col>

  <v-row>
      <v-col>
          <DisclaimerShow/>
      </v-col>
      <v-col>
        <LicenseShow/>
      </v-col>
  </v-row>
</template>

<script>
import FileUpload from '../components/FileUpload.vue'
import DisclaimerShow from './DisclaimerShow.vue';
import LicenseShow from './LicenseShow.vue';

export default {
    name: "Electronic Health Record Analysis Home",
    components: { FileUpload, DisclaimerShow, LicenseShow },
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
            myTargetURL: "ehr",
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

        downloadItem () {
            // Depending on how we proceed, see here for download support:
            // https://stackoverflow.com/questions/53772331/vue-html-js-how-to-download-a-file-to-browser-using-the-download-tag
            //
            alert("File download is not yet supported");
            console.log("---> File download is not yet supported");
        },
    }
}


</script>