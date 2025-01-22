<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
            <!--
                See `rules` for filtering on file type. 
                Not super critical at present. 
             -->
  <v-container :key="action">
    Current key: {{ action }}
  </v-container>
  <v-row>
    <v-col cols="4">
      <v-radio-group v-model="action" v-on:change="getModels">
        <v-radio label="Train new models" value="training"></v-radio>
        <v-radio label="New sample with trained model" value="newSample"></v-radio>
      </v-radio-group>
    <v-card flat :key="action" v-if="action === 'newSample'">
      <v-card-title>Available models</v-card-title>
      <v-list>
        <v-list-item
          v-for="obj in availableModels"
          :key="obj"
          :title="'Name: ' + obj.name"
          :subtitle="'Pickle: ' + obj.pickle"
        ></v-list-item>
      </v-list>
    </v-card>
    </v-col>
    <v-col cols="8">
      <v-file-input
            show-size
            label="Training set or new sample to use with prior models."
            type="File"
            clearable
            v-model="currentFile"
          ></v-file-input>
      <v-text-field 
        hint="Response data column for prediction"
        persistent-hint
        type="input"
        v-model="labelColumn"
        >
      </v-text-field>
      <v-text-field 
        hint="Columns that need to be removed from the data set (comma-separated)"
        persistent-hint
        type="input"
        v-model="columnsToDrop"
        >
      </v-text-field>
    </v-col>
  </v-row>
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
            @click="importFileAndScan" 
            v-if="!uploadSuccess">
            Submit File
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
          </v-btn>
          <v-btn
            @click="logResponseToConsole"
          >Report result field</v-btn>
        </v-col>
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
      <v-row class="pa-5" v-if="response">
          <PipelineResultsCard 
            :data="response"
          />
      </v-row>
    </v-container>
  </template>
  
  <script>

import UploadService from "@/services/UploadService";
import PipelineResultsCard from "@/components/PipelineResultsCard.vue";
import { useUserStore } from "@/store/user";
import * as XLSX from 'xlsx';

  export default {
    name: "upload-files",
    props: {
        uploadTargetURL: String,
        modelsURL: String,
    },
    setup() {
      const userStore = useUserStore();
      return { userStore }
    },
    components: { PipelineResultsCard, UploadService },
    data() {
      return {
        baseURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + "/api": "/predictmod/api",
        currentFile: null,
        response: null,
        progress: 0,
        message: "Data must be selected before results are available",
        labelColumn: "",
        columnsToDrop: [],
        error: null,
        uploadSuccess: false,
        counterToken: 0,
        action: "training",
        availableModels: [],
      };
    },
    methods: {
        checkUser() {
          // console.log("Checking user ROLE: ", this.userStore.role);
          return this.userStore.role > 2;
        },
        // XXX
        // getFileLabelText() {
        //   if (this.action === "training") {
        //     return "Provide training data in xls or xlsx file format. Row 1=Column headings, Row 2..N=Data samples"
        //   } else if (this.action === "newSample") {
        //     return "Select a model to use and provide a sample in xls or xlsx format. Row 1=Column headings, Row 2=New data sample"
        //   } else {
        //     return "Error state: Action is " + this.action
        //   }
        // },
        // XXX
        forceRedraw() {
          this.counterToken += 1;
        },
        logResponseToConsole() {
          console.log(this.response);
        },
        async getModels() {
          if (this.action === 'training') {
            return
          }
          const modelsURL = this.baseURL + '/' + this.modelsURL
          console.log("---> Called get models. Collecting from " + modelsURL)
          const response = await fetch(modelsURL, {
            credentials: "include",
          })
          const models = await response.json()
          console.log("Got response ", JSON.stringify(models))
          if (!response.ok) {
            // Error handling
          } else {
            this.availableModels = models.models_available
          }
          
        },
        importFileAndScan() {
            if (!this.currentFile) {
                this.message = null;
                this.error = "Please select a file for upload!"
                return;
            }
            // console.log("---> Now attempting to read file");
            const reader = new FileReader();
            reader.readAsArrayBuffer(this.currentFile);
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
          this.message = null;
          this.error = "Please select a file for upload!";
          return false;
        }
        if (!this.data) {
          this.message = null;
          this.error = "Please upload a data file!";
          return false;
        }
        if (!this.labelColumn) {
          this.message = null
          this.error = "There must be exactly one column of labelled outcomes"
          return false
        }
  
        this.error = null

        UploadService.upload(this.data, this.uploadTargetURL, (event) => {
          this.progress = Math.round((100 * event.loaded) / event.total);
        }, this.labelColumn, this.columnsToDrop, this.action)
          .then((response) => {
            // this.message = response.data.message;
            // console.log("Got response:\n", response);
            this.message = "Success";
            this.response = response;
            if (response.error) {
              console.log("ERROR: ", response.error);
              this.error = response.error;
              // this.standIn = true;
            }
            return true;
          })
          .catch(() => {
            this.progress = 0;
            this.message = null;
            this.error = "Could not upload the file!";
            // this.currentFile = null;
            // this.data = null;
            return false;
          });
      },
    },
  };

  </script>