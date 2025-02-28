<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
  <v-file-input
        show-size
        label="Training set or new sample to use with prior models."
        type="File"
        clearable
        v-model="currentFile"
      ></v-file-input>
  <v-text-field
    hint="Name of model or data type for later re-use"
    persistent-hint
    type="input"
    v-model="modelName"  
  >
  </v-text-field>
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
  <!-- </v-row> -->
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
    name: "automated-pipeline-train",
    props: {
        uploadTargetURL: String,
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
        modelName: "",
        labelColumn: "",
        columnsToDrop: [],
        error: null,
        uploadSuccess: false,
        counterToken: 0,
      };
    },
    methods: {
        checkUser() {
          // console.log("Checking user ROLE: ", this.userStore.role);
          return this.userStore.role > 2;
        },
        forceRedraw() {
          this.counterToken += 1;
        },
        logResponseToConsole() {
          console.log(this.response);
        },
        importFileAndScan() {
            if (!this.currentFile) {
                this.message = null;
                this.error = "Please select a file for upload!"
                return
            }
            this.uploadSuccess = this.upload();
        },
  
      upload() {
        if (!this.currentFile) {
          this.message = null;
          this.error = "Please select a file for upload!";
          return false;
        }
        if (!this.labelColumn) {
          this.message = null
          this.error = "There must be exactly one column of labelled outcomes"
          return false
        }
  
        this.error = null

        // TODO: Axios progress on upload
        // const onProgressBar = (event) => {
        //   this.progress = Math.round((100 * event.loaded) / event.total);
        // }

        UploadService.upload(this.currentFile, this.uploadTargetURL, {}, {
          action: "training",
          labelColumn: this.labelColumn,
          columnsToDrop: this.columnsToDrop,
          modelName: this.modelName,
        })
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