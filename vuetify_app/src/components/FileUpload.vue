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
      <v-row class="pa-5" v-if="showChart">
        <StandinChart v-if="standIn" />
        <SHAPForcePlot 
          v-if="chartData" 
          :chart-data="chartData" 
          :key="counterToken"
        />
        <v-img 
          v-if="imageData" 
          :src="imageData"
          :height="600"
          :width="1000"
          height
        />
        <v-btn @click="forceRedraw()">Redraw!</v-btn>
      </v-row>
    </v-container>
    </div>
  </template>
  
  <script>

import UploadService from "@/services/UploadService";
  import StandinChart from "@/components/StandinChart.vue";
  import SHAPForcePlot from "@/components/SHAPForcePlot.vue";
  import * as XLSX from 'xlsx';

  export default {
    name: "upload-files",
    props: {
        uploadTargetURL: String,
    },
    components: { SHAPForcePlot, StandinChart },
    data() {
      return {
        currentFile: null,
        data: null,
        chartData: null,
        imageData: null,
        standIn: false,
        progress: 0,
        message: "Data must be selected before results are available",
        showChart: false,
        uploadSuccess: false,
        counterToken: 0,
      };
    },
    methods: {
        forceRedraw() {
          this.counterToken += 1;
        },
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
            if (response.plot) {
              this.chartData = JSON.parse(response.plot);
            }
            else if (response.image) {
              this.imageData = "data:image/png; base64, " + response.image;
              console.log("Image data is now: %s", this.imageData)
            }
            else {
              this.standIn = true;
            }
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