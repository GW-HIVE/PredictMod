<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
  <!--
  <v-col cols="11">
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
    </div>
    </v-col>
  -->
      <!-- <v-row no-gutters justify="center" align="center"> -->
        <!-- <v-col cols="8"> -->
        <!-- <v-col> -->
            <!--
                See `rules` for filtering on file type. 
                Not super critical at present. 
             -->
          <v-file-input
            show-size
            v-if="this.checkUser()"
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
            v-if="this.checkUser() && !uploadSuccess">
            Submit & Analyze
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
          </v-btn>
          <v-btn 
            color="primary"
            v-if="!this.checkUser()"
            @click="exampleAnalysis"
          >
            Example Analysis
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
      <v-alert v-if="error" color="red" class="pa-5">
        {{ error }}
      </v-alert>
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
        <!-- <v-btn 
          @click="console.log('Toggling! %s', toggleOverlay); toggleOverlay = !toggleOverlay"
          > -->
        <v-card 
          variant="elevated"
          @click="toggleOverlay = !toggleOverlay"
        >
          <v-card-text>
            SHAP Force Plot - Click to expand
          </v-card-text>
        <v-img
          :src="imageData"
          :height="200"
          :width="1000"
          rounded="shaped"
          
          height
        />
      </v-card>
        <!-- </v-btn> -->
        
      </v-row>
    </v-container>
        <v-container>
        <v-overlay
          v-model="toggleOverlay"
          @click.prevent="toggleOverlay = !toggleOverlay"
          class="d-flex align-center justify-center"
          >
        <v-card
        >
        <v-img
          :src="imageData"
          height="300"
          width="1200"
        ></v-img>
        </v-card>
        </v-overlay>
        </v-container>
        <!-- <v-btn @click="forceRedraw()">Redraw!</v-btn> -->


  </template>
  
  <script>

import UploadService from "@/services/UploadService";
import StandinChart from "@/components/StandinChart.vue";
import SHAPForcePlot from "@/components/SHAPForcePlot.vue";
import { useUserStore } from "@/store/user";
import * as XLSX from 'xlsx';

  export default {
    name: "upload-files",
    props: {
        uploadTargetURL: String,
        modelsToUse: Array || null,

    },
    setup() {
      const userStore = useUserStore();
      return { userStore };
    },
    components: { SHAPForcePlot, StandinChart },
    data() {
      return {
        currentFile: null,
        chartData: null,
        imageData: null,
        toggleOverlay: false,
        standIn: false,
        progress: 0,
        message: "Data must be selected before results are available",
        error: null,
        showChart: false,
        uploadSuccess: false,
        counterToken: 0,
      };
    },
    methods: {
        checkUser() {
          // console.log("Checking user ROLE: ", this.userStore.role);
          return this.userStore.role > 0;
        },
        forceRedraw() {
          this.counterToken += 1;
        },
    async exampleAnalysis() {
      console.log("===> Launching pre-loaded example analysis")
        let baseURL = ""
        if (import.meta.env.DEV) {
          baseURL = import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api'
        } else if (import.meta.env.PROD) {
          if (import.meta.env.VITE_PRODUCTION_HOST == 'local'){
            baseURL = import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE + '/api'
          } else {
            baseURL = import.meta.env.VITE_PROD_MIDDLEWARE_BASE + '/api'
          }
        }
        const model = this.uploadTargetURL
        const exampleURL = baseURL + `/upload/?q=${model}&name=example`
        console.log("===> Requesting analysis from " + exampleURL)
        const res = await fetch(exampleURL, {
          method: "POST",
          credentials: "include",
          headers: {
            // "Accept": "application/json",
            // "Content-Type": "multipart/form-data",
            "X-CSRFToken": this.userStore.token,
          },
          body: {},
        })

        if (!res.ok) {
          // Error handling
          // console.log("Result was not OK:\n" + JSON.stringify(res))
          const response = await res.json()
          if (response) {
            // console.log("Got a response in error: " + JSON.stringify(response))
            return { networkError: response.error }
          }
          return {
            networkError: "Error " + res.status + ":" + res.statusText,
          }
        }

        const response = await res.json();
        // console.log("===> Got response: " + JSON.stringify(response))
        
        this.message = response.result ? response.result : null;
        if (response.plot) {
          this.chartData = JSON.parse(response.plot);
          this.showChart = true;
        }
        else if (response.image) {
          this.imageData = "data:image/png; base64, " + response.image;
          this.showChart = true;
          // console.log("Image data is now: %s", this.imageData)
        }
        else if (response.error) {
          console.log("ERROR: ", response.error);
          this.error = response.error;
          this.showChart = false;
          // this.standIn = true;
        }

    },
        importFileAndAnalyze() {
            if (!this.currentFile) {
                this.message = null;
                this.error = "Please select a file for upload!"
                return;
            }
            console.log("---> Now attempting to read file: " + this.currentFile);
            this.uploadSuccess = this.upload();
        },
  
      upload() {
        if (!this.currentFile) {
          this.message = null;
          this.error = "Please select a file for upload!";
          return false;
        }

        if (this.currentFile.size > 31457280) { // ~30 MB Hardlimit. Apache/nginx configured for 50 MB
          this.message = null;
          this.error = "Maximum file upload size is 25 MB. Please contact mazumder_lab@gwu.edu for additional support"
          this.currentFile = null
          return false
        }

        const fileType = this.currentFile.name.split(".").at(-1)

        if ((fileType == "xlsx" || fileType == "xls") && this.currentFile.size > 2097152) {
          // Excel over 2 MB is too slow to support on the backend, accept only csv or tsv at this size
          this.message = null
          this.error = "Excel files over 2 MB are not supported; please convert to csv or tsv formats"
          this.currentFile = null
          return false
        }

        // TODO
        // const onUploadProgress = (event) => {
        //   this.progress = Math.round((100 * event.loaded) / event.total)
        // }

        // const config = {
        //   // onUploadProgress: onUploadProgress ^^^
        //   headers: {
        //     "Content-Type": "multipart/form-data",
        //     "X-CSRFToken": this.userStore.token,
        //   }
        // }

        UploadService.upload(this.currentFile, this.uploadTargetURL, {})
          .then((response) => {
            // this.message = response.data.message;
            // console.log("Got response:\n", response);
            if (response.networkError) {
              this.message = null
              this.error = "Error on upload: Response code " + response.error
              return false
            }
            this.message = response.result ? response.result : null;
            if (response.plot) {
              this.chartData = JSON.parse(response.plot);
              this.showChart = true;
            }
            else if (response.image) {
              this.imageData = "data:image/png; base64, " + response.image;
              this.showChart = true;
              // console.log("Image data is now: %s", this.imageData)
            }
            else if (response.error) {
              console.log("ERROR: ", response.error);
              this.error = response.error;
              this.showChart = false;
              // this.standIn = true;
            }
            return true;
          })
          .catch(() => {
            this.progress = 0;
            this.message = null;
            this.error = "Could not upload the file!";
            // this.currentFile = null;
            return false;
          });
      },
    },
  };

  </script>