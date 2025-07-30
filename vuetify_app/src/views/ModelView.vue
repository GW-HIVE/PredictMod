<template>
  <v-app>
  <v-navigation-drawer
    width="800"
    location="left"
    v-model="queryState.downloadDrawer"
    temporary
    persistent
  >
  <v-col pa="2">
      <v-row class="justify-end">
        <v-alert
          v-if="this.previewMessage"
          type="warning"
          v-text="this.previewMessage"
          fluid
        ></v-alert>
        <!-- <v-spacer></v-spacer> -->
        <v-btn color="primary" @click.prevent="downloadFromPreview">
          Download
        </v-btn>
        <v-btn @click.prevent="queryState.downloadDrawer = !queryState.downloadDrawer">
          Cancel
        </v-btn>
      </v-row>
  </v-col>
    <Spreadsheet 
          :sheet-data="gridData" 
          v-if="queryState.downloadDrawer"
          :key="gridData"
          />
        <!-- <canvas-datagrid 
          :data.prop="gridData" 
          autoResizeRows.prop
          canvas.prop=""
        /> -->

  </v-navigation-drawer>
    <v-banner
    single-line
    class="text-left">
      <v-img
        src="../assets/Welcome_Header.jpg"
        id="intro-img"
        gradient="to bottom, rgba(119, 119, 119, 0.25), rgba(0, 0, 0, 0.75)"
        :height="400" 
        :cover="true"
        >
        <div class="d-flex fill-height" style="flex-direction:column">
            <div class="d-flex fill-height align-center justify-center"> 
              <v-card flat color="transparent">
              <v-card-title class="title text-center font-weight-bold">
                <h1>PredictMod Models</h1>
              </v-card-title>
              <!-- <v-card-text class="text-center">
                A Machine Learning-Based Application for Informed Clinical Decision Making
              </v-card-text> -->
              </v-card>
        <!-- <span class="introduction">PredictMod Test Text</span> -->
        </div>
        </div>
      </v-img>
    </v-banner>
  
    <v-container fluid>
      <h1>{{ convertedModelName }}</h1>
    </v-container>
  <v-container fluid>
    <div v-html="modelDetails" v-if="showDetails" style="text-align: justify">
    </div>
  </v-container>
  <v-container v-if="modelMetaData">
    <MetadataDashboard :metadata=modelMetaData />
  </v-container>

<!-- <v-btn @click.submit="getMarkDown()">Test getting markdown</v-btn> -->
<v-container>

  <ToolControlPanel target-u-r-l="modelsURL" :model-name="name" :model-view=true />

</v-container>
<v-container>

  <AIInterface v-if="modelInitialQuery" :initial-query="modelInitialQuery" :model-name="name"/>
</v-container>
<v-container>
      <!-- <v-btn @click.submit="logModels()">Click to log models to console</v-btn> -->
  
      <v-row>
        <v-col>
          <DisclaimerShow/>
        </v-col>
        <v-col>
          <LicenseShow/>
        </v-col>
      </v-row>
  
  
  </v-container>
  
  <!-- <v-img src="../assets/Footer.png">
    
  </v-img> -->
  </v-app>
  
  </template>
  <script>
  import { onMounted, ref } from 'vue';
  import { useAppStore } from '@/store/app';
  import { useQueryState } from '@/store/queryState';
  import ToolControlPanel from '@/components/ToolControlPanel.vue';
  import DownloadService from '@/services/DownloadService';
  import DisclaimerShow from './DisclaimerShow.vue';
  import Spreadsheet from '@/components/Spreadsheet.vue';

  import NotFound from './NotFound.vue';
  import LicenseShow from './LicenseShow.vue';
  
  import { marked } from "marked";
  import * as XLSX from 'xlsx';
import MetadataDashboard from '@/components/MetadataDashboard.vue';
import AIInterface from '@/components/AIInterface.vue';

  const modelsURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/model-details/': "/predictmod/api/model-details/";
  
  export default {
  
    name: 'Models',
    setup() {
    //   console.log("---> Model view, initializing")
      const appStore = useAppStore();
      const queryState = useQueryState();
      return { appStore, queryState };
    },
    mounted() {
      if (!this.appStore.releasedModels) {
        this.appStore.getModels();
      };
      this.getMarkDown();
      // this.getAiResponse();
    },
    props: {
        name: String,
    },
    data() {
        return {
            modelsURL: modelsURL,
            previewMessage: "",
            showDetails: false,
            modelDetails: null,
            modelMetaData: null,
            modelInitialQuery: "",
            queryAI: false,
        }
      },
    computed: {
      gridData() {
        if (!this.queryState.filePreviewData) {
          console.log("Query State: no file preview!!!")
          return [];
        }
        const data = JSON.parse(this.queryState.filePreviewData);
        if (data.length > 500) {
          this.previewMessage = "Download file too large to display, preview is truncated"
          console.log("Truncating data - length was " + data.length)
          return data.slice(0, 500)
        }
        const keys = Object.keys(data[0])
        const dataWidth = keys.length
        const maxWidth = 100
        if (dataWidth > maxWidth) {
          this.previewMessage = `Downloaded file too wide to display, only first row and ${maxWidth} columns shown`
          const newArray = new Array()
          const newDataObject = {}
          for (const key of keys.slice(0, maxWidth)) {
            newDataObject[key] = data[0][key]
          }
          newArray.push(newDataObject)
          return newArray
        }
        return data;
      },
      convertedModelName() {
        return this.name.replace(/[-_]/g, ' ')
      },
    },
    methods: {
      async getMarkDown() {
        const localURL = `${this.modelsURL}?q=${this.name}`
        // console.log("Getting details for: ", localURL);
        const res = await fetch(localURL, {
            method: 'GET',
        });
        if (!res.status == 200) {
            console.log("Error on return")
        };
        const response = await res.json();
        // console.log("Received response:\n", JSON.stringify(response));
        this.modelDetails = marked.parse(response.details);
        if (response.metadata) {
          this.modelMetaData = response.metadata
          response.metadata?.search_terms 
            // console.log("Got search terms\n" + JSON.stringify(response.metadata.search_terms))
            this.modelInitialQuery = response.metadata.search_terms
        }
        this.showDetails = true;
      },
      downloadFromPreview() {
        if (!this.queryState.filePreviewData) {
          // Error handling
          return false;
        }
        // const data = this.gridData;
        const data = JSON.parse(this.queryState.filePreviewData);
        // console.log("Downloading data:\n%s", data);
        const sampleName = this.name + ".xlsx";
        // Write the response to a file
        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet);
        XLSX.writeFile(workbook, sampleName, { compression: true });
        return true;
      },
    },
    components: { AIInterface, MetadataDashboard, ToolControlPanel, Spreadsheet, DisclaimerShow, LicenseShow }
  }
  </script>
  