<template>
  <!-- <v-navigation-drawer
    location="left"
    temporary
  > -->
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
              <h1>Run a Sample Prediction</h1>
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
    <v-col cols="11">
    <v-row>
      <v-col>
        <h4>Step 1: Select medical condition</h4>
        <QueryCard
        :key="queryState.conditions"
        @confirmed="confirmCondition"
        @unconfirmed="unconfirmCondition"
          target-prop="condition"
          :menuItems="queryState.conditions"
          :title="'Condition'"
        />
      </v-col>
    <v-col cols="1">
      <v-btn
      @click.prevent="resetState"
      fab
      position="fixed"
      size="large"
      color="primary"
      elevation="0"
      rounded="xl0">
      <small>Restart query</small>
      </v-btn>
      <!--
    <v-col cols="1">
      <v-row>
       <v-btn
        @click.prevent="togglePreview"
        fab
        position="fixed"
        size="large"
        elevation="0"
        rounded="xl0">
      <small>Toggle Preview</small>
      </v-btn>
    </v-row>
    </v-col>
  -->
  </v-col>
    </v-row>
    <v-col cols="11">
      <v-row v-if="queryState.condition">
        <h4>Step 2: Select intervention type</h4>
        <QueryCard :key="queryState.interventions"
        @confirmed="confirmCondition"
        @unconfirmed="unconfirmCondition"
        target-prop="intervention"
          :menuItems="queryState.interventions" 
          :title="'Intervention'"
        />
      </v-row>
    </v-col>
    <v-col cols="11">
      <v-row v-if="queryState.condition">
        <h4>Step 3: Select available data format</h4>
        <QueryCard :key="queryState.dataTypeOptions"
        @confirmed="confirmCondition"
        @unconfirmed="unconfirmCondition"
        target-prop="datatype"
          :menuItems="queryState.dataTypeOptions" 
          :title="'Data Provenance'"
        />
    </v-row>
    </v-col>
  </v-col>

    <!-- <v-btn
      elevation="2"
      fab
      @click="resetState()"
    >
      Reset Query
    </v-btn> -->

    <v-container 
      v-if="queryCompleted">
      <v-col cols="11">
      <v-row class="justify-center pa-2">
      <br>
        <h4>Step 4: Interact with the model</h4>
      <br>
      </v-row>
      <v-row class="justify-center pa-2">
      <ToolControlPanel />
      <!-- <ToolControlPanel
        :selections="selections" 
        :target-u-r-l="myTargetURL" 
        :model-anchor="modelAnchor"
      /> -->
    </v-row>
  </v-col>
    </v-container>
    <v-row>
      <v-col>
        <DisclaimerShow/>
      </v-col>
      <v-col>
        <LicenseShow/>
      </v-col>
    </v-row>


</v-container>
</v-app>
<!-- <v-img src="../assets/Footer.png">
  
</v-img> -->


</template>
<script>
import { onMounted, ref } from 'vue';
import { useQueryState } from '@/store/queryState';
import * as XLSX from 'xlsx';

import QueryCard from '@/components/QueryCard.vue';
import Spreadsheet from '@/components/Spreadsheet.vue';
import ToolControlPanel from '@/components/ToolControlPanel.vue';
import DisclaimerShow from './DisclaimerShow.vue';
import LicenseShow from './LicenseShow.vue';

export default {

  name: 'QueryBuilder',
  setup() {
    const queryState = useQueryState();
    return { queryState }
  },
  mounted() {
    this.queryState.populateOptions();
    // this.getConditions();
  },
  computed: {
    queryCompleted() {
      return (
        this.queryState.condition !== null && 
        this.queryState.intervention !== null &&
        this.queryState.datatype !== null
      );
    },
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
  },
  data() {
			return {
        conditionSet: false,
        interventionSet: false,
        inputTypeSet: false,
        showToolbar: false,
        cdg: null,
        myTargetURL: "",
		}
  },
  methods: {
    downloadFromPreview() {
      if (!this.queryState.filePreviewData) {
        // Error handling
        return false;
      }
      const data = JSON.parse(this.queryState.filePreviewData);
      const sampleName = this.queryState.targetURL;
      // console.log("---> Data (Type %s):\n%s", typeof(data), JSON.stringify(data));
      // console.log("---> Attempting to write to %s", sampleName);
      // Write the response to a file
      // console.log("Creating sheet!")
      const worksheet = XLSX.utils.json_to_sheet(data);
      // console.log("Creating workbook!")
      const workbook = XLSX.utils.book_new();
      // console.log("Appending sheet!")
      XLSX.utils.book_append_sheet(workbook, worksheet);
      // console.log("Writing file!")
      XLSX.writeFile(workbook, sampleName, { compression: true });
      // console.log("Complete...?")
      return true;
    },
    getConditions() {
      this.conditions = this.queryState.getConditions();
    },
    confirmCondition(condition, selection) {
      // console.log("Handling message from query: %s", selection);
      this.queryState.setState(condition, selection);
      if (this.queryCompleted) {
        this.queryState.registerURL();
        this.queryState.setTargetAnchor();
      }
    },
    unconfirmCondition(condition) {
      switch (condition) {
        case 'condition':
          this.queryState.setState(condition, null);
          this.queryState.populateOptions();
          break;
        case 'intervention':
        case 'datatype':
          this.queryState.setState(condition, null);
          break;
        default:
          console.log("Invalid option %s", condition);
      }
      if (!this.queryCompleted) {
        this.queryState.registerURL();
        this.queryState.setTargetAnchor;
      }
    },

    setTargetAnchor() {
      const baseString = "/predictmod/help#current-models"
      switch (this.myTargetURL) {
          case "mg":
              this.modelAnchor = baseString + "-mg-exercise";
              break;
          case "ehr":
              this.modelAnchor = baseString + "-ehr-diet-counseling";
              break;
          default:
              this.modelAnchor = "/predictmod/NotFound";
      }
    },
    resetState() {
      // console.log("---> Resetting query state");
      this.queryState.resetState();
      this.queryState.filePreviewData = null;
      this.unconfirmCondition('condition');
    },
    // XXX
    reportData() {
      if (this.queryState.filePreviewData) {
        console.log("Query preview data:\n%s", JSON.stringify(
          this.queryState.filePreviewData
        ));
        console.log("---> Download drawer toggle: %s", this.queryState.downloadDrawer);
      } else {
        console.log("===> No file preview data available <===");
      }
      ;
    },
    togglePreview() {
      this.queryState.downloadDrawer = !this.queryState.downloadDrawer;
    },
  },
  components: { QueryCard, Spreadsheet, ToolControlPanel, DisclaimerShow, LicenseShow }
}
</script>
