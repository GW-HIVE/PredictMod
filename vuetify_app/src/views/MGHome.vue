<template>
<v-banner
  single-line
  class="text-center"
  >
    <v-img
      src="../assets/MG_Model.jpg"
      id="intro-img"
      gradient="to bottom, rgba(119, 119, 119, 0.25), rgba(0, 0, 0, 0.75)"
      :height="400" 
      :cover="true"
      >
      <div class="d-flex fill-height" style="flex-direction:column">
          <div class="d-flex fill-height align-center justify-center"> 
            <v-card flat color="transparent">
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
            </v-card>
          </div>
        </div>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

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
        <FileDownload :download-target-u-r-l="myTargetURL" />
        <!-- <a>
          <v-btn elevation="0" border @click.prevent="downloadItem(item)">
              Download Example File
          </v-btn>
        </a> -->
      </v-container>
    </v-row>
    <v-container>
    <v-row class="justify-center">
      <v-card-title class="title text-center font-weight-bold" >
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
      </v-card-title>
    </v-row>
  </v-container>
  </div>

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
// import GetMGoutput from './GetMGoutput.vue'
import FileUpload from '../components/FileUpload.vue';
import FileDownload from '@/components/FileDownload.vue';
import DisclaimerShow from './DisclaimerShow.vue';
import LicenseShow from './LicenseShow.vue';

import axios, { Axios } from 'axios';

export default {
    name: "Metagenomic Analysis Home",
    components: { FileUpload, FileDownload, DisclaimerShow, LicenseShow },
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
                "Keto Diet",
                "Diabetes Managed by Diet",
            ],
            interventionType: "Intervention Type",
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

        downloadItem () {
            // Depending on how we proceed, see here for download support:
            // https://stackoverflow.com/questions/53772331/vue-html-js-how-to-download-a-file-to-browser-using-the-download-tag
            //
            const warning = "This service is still under development"
            // const warning = "Download service is not yet supported"
            console.log(warning);
            alert(warning);

            // TODO: Enable downloads
            // const data = DownloadService.download(this.myTargetURL);

            // const csv = '';
            // data.array.forEach((row) => {
            //   csv += row.join(',');
            //   csv += "\n";
            // });

            // const anchor = document.createAttribute('a');
            // anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
            // anchor.target = '_blank';
            // anchor.download = 'metagenomic_example_data.csv';
            // anchor.click();
            // XXX

            // TODO: This currently returns the (what appears to be...) correct binary information, but
            // Excel complains that the file is corrupt. :/ 

            // axios.get("http://localhost:5000/metagenomic-download")
            //   .then(response => {
            //     const blob = new Blob([response.data], {type: 'application/vnd.ms-excel'});
            //     const link = document.createElement('a');
            //     link.href = URL.createObjectURL(blob);
            //     link.download = 'metagenomic_sample_data.xls';
            //     link.click();
            //     URL.revokeObjectURL(link.href);
            //   }).catch(console.error)
        },
    }
}


</script>