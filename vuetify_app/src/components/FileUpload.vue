<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
    <div class="text-center">
      <div>
        <div>
          <v-progress-linear
            v-model="progress"
            color="light-blue"
            height="25"
            reactive
          >
            <strong>{{ progress }} %</strong>
          </v-progress-linear>
        </div>
      </div>
  
      <!-- <v-row no-gutters justify="center" align="center"> -->
        <!-- <v-col cols="8"> -->
        <!-- <v-col> -->
            <!--
                See `rules` for filtering on file type. 
                Not super critical at present. 
             -->
          <v-file-input
            show-size
            label="Select a PredictMod-formatted xls or xlsx file"
            type="File"
            v-model="currentFile"
          ></v-file-input>
        <!-- </v-col> -->
        <!--
            This appears to break when invoked using Vuetify auto-magic 
            @change="selectFile($event)" 
        -->
            
        <!-- <v-col cols="4" class="pl-2"> -->
        <v-container class="justify-center">
        <v-row>
        <v-col class="justify-center">  
          <v-btn 
            color="primary"
            :key="uploadSuccess" 
            @click="importFileAndAnalyze" 
            v-if="!uploadSuccess">
            Submit & Analyze
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
          </v-btn>
        </v-col>
        <!-- <v-col>
          <v-btn right color="success" dark small @click="upload">
            Submit & Analyze
          </v-btn>
        </v-col> -->
      </v-row>
    </v-container>
      <!-- </v-row> -->
      <v-container>
      <v-alert v-if="message" color="blue-grey" class="pa-5" dark>
        {{ message }}
      </v-alert>
      <v-row class="pa-5">
        <Chart v-if="showChart" /> 
      </v-row>
    </v-container>
    </div>
  </template>
  
  <script>
  import UploadService from "@/services/UploadService";
  import Chart from "@/components/Chart.vue";

  import * as XLSX from 'xlsx';

  export default {
    name: "upload-files",
    props: {
        uploadTargetURL: String,
    },
    components: { Chart },
    data() {
      return {
        currentFile: null,
        data: null,
        progress: 0,
        message: "Data must be selected before results are available",
        showChart: false,
        uploadSuccess: false,
      };
    },
    methods: {
        importFileAndAnalyze() {
            if (!this.currentFile) {
                this.message = "Please select a file for upload!"
                return;
            }
            // console.log("---> Now attempting to read file");
            const reader = new FileReader();
            reader.readAsArrayBuffer(this.currentFile[0]);
            // console.log("---> Reader has read the file!");
            reader.onload = (event) => {
                const rawData = reader.result;
                const workbook = XLSX.read(rawData);
                const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                const arrayedData = XLSX.utils.sheet_to_json(firstSheet, {header: 1});
                this.data = JSON.stringify(arrayedData);
                // console.log("Now we have data:\n%s", this.data);
                this.uploadSuccess = this.upload();
            }
        },
  
      upload() {
        if (!this.currentFile) {
          this.message = "Please select a file for upload!";
          return;
        }
        if (!this.data) {
          this.message = "Please upload a data file!";
          return;
        }
  
        UploadService.upload(this.data, this.uploadTargetURL, (event) => {
          this.progress = Math.round((100 * event.loaded) / event.total);
        })
          .then((response) => {
            // this.message = response.data.message;
            this.message = response.result ? response.result : response.error;
            this.showChart = true;
            return true;
          })
          .catch(() => {
            this.progress = 0;
            this.message = "Could not upload the file!";
            // this.currentFile = null;
            // this.data = null;
            return false;
          });
      },
    },
  };

  </script>