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
        :key="queryState.condition"
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
        <QueryCard :key="queryState.condition"
        @confirmed="confirmCondition"
        @unconfirmed="unconfirmCondition"
        target-prop="intervention"
          :menuItems="queryState.interventionOptions" 
          :title="'Intervention'"
        />
      </v-row>
    </v-col>
    <v-col cols="11">
      <v-row v-if="queryState.condition">
        <h4>Step 3: Select available data format</h4>
        <QueryCard :key="queryState.condition"
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
        return [];
      }
      // console.log("---> Computing worksheet <---")
      const data = JSON.parse(this.queryState.filePreviewData);

      // const wb = XLSX.read(data);
      // const ws = wb.Sheets[wb.SheetNames[0]];
      // const sheetData = XLSX.utils.sheet_to_json(ws, { header:1 });
      
      // if (!this.cdg) {
      //   this.cdg = canvasDatagrid({
      //     parentNode: this.$refs.gridContainer.$el,
      //     data
      //   })
      // } else {
      //   this.cdg.data = data;
      // }

      return data;
    },
    // columns() {
    //   if (!this.queryState.filePreviewData) {
    //     return [];
    //   }
    //   return Object.keys((JSON.parse(this.queryState.filePreviewData))[0]).forEach(k => {
    //     console.log("Computing name %s", k)
    //     return { field: k, label: k }
    //   })
    // },
    // rows() {
    //   if (!this.queryState.filePreviewData) {
    //     return [];
    //   }
    //   return Object.values((JSON.parse(this.queryState.filePreviewData))[0]).forEach(v => {
    //     return { name: v }
    //   })
    // },
  },
  data() {
			return {
        conditionSet: false,
        interventionSet: false,
        inputTypeSet: false,
        showToolbar: false,
        cdg: null,
        // conditions: [],
        // interventions: [],
        // dataInputTypes: {},
			// 	home: false,
      //   interventionRelay: {},
      //   dataTypeRelay: {},
      //   selections: {},
        myTargetURL: "",
      //   modelAnchor: "",
        
      // conditions: [
      //     {
      //       name: "Prediabetes",
      //       description: `A precursor to Type 2 Diabetes Mellitus (T2DM), where blood sugars are higher than normal, 
      //       but not high enough to be considered T2DM. Prediction outcomes are based 
      //       on a 5% reduction in weight, HOMA-IR, or a diagnosis of T2DM.`
      //     },
      //     {
      //       name: "Epilepsy",
      //       description: 
      //           `A neurological disorder in which nerve cell activity in the brain 
      //           is disturbed, causing seizures. Prediction outcomes are based on [TBD].`
      //     },
      //     {
      //       name: "Renal Carcinoma",
      //       description: `[TBD]`,
      //     },
      //   ],

        // interventions:
      //   {
          // 'Prediabetes':
          //   [
          //     {name: "Diet - Dietary Counseling", description: "Involves following a physician-recommended diet for the management of prediabetes."},
          //     {name: "Diet - Keto Diet", description: "A low-carb, ketogenic diet commonly recommended for the management of prediabetes."},
          //     {name: "Exercise", description: "Involves following a physician-recommended exercise regimen for the management of prediabetes."},
          //     {name: "Medication - Semaglutide", description: "Medication management of prediabetes using an increasingly popular GLP1-agonist."},
          //     {name: "No Intervention", description: "Predictions based on existing biomarkers. These predictions do not involve a specific intervention."},
          //   ],
          // 'Epilepsy':
          // [
          //   {name: "TBD", description: "TBD"},
          // ],
          // 'Renal Carcinoma':
          // [
          //   {name: "TBD", description: "TBD"},
          // ],
      //   },

      // urlTargets: {
        // "Prediabetes": 
        //   {
        //     "EHR": "ehr",
        //     "Gut Microbiome": "mg",
        //   },
        // "Epilepsy": {},
        // "Renal Carcinoma": {},
      // },

      // dataInputTypes:
      //   {
        //   'Prediabetes': 
        //   [
        //     {name: "EHR", description: "Data sourced from clinical Electronic Health Records ,e.g. EPIC-COSMOS or MDClone"},
        //     {name: "Gut Microbiome", description: "Microflora population and diversity information measured via High Throughput Sequencing"},
        //     {name: "Glycoproteomics", description: "TBD"},
        //     {name: "Glycomics", description: "TBD"},
        //   ],
        //  'Epilepsy':
        //   [
        //     {name: "TBD", description: "TBD"},
        //   ],
        //   'Renal Carcinoma':
        // [
        //   {name: "TBD", description: "TBD"},
        // ],
      // },
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
      // this.interventionRelay = this.interventions[selection];
      // this.dataTypeRelay = this.dataInputTypes[selection];
      // this.selections['Condition'] = selection;
      // this.conditionSet = true;
      if (this.queryCompleted) {
        this.queryState.registerURL();
        this.queryState.setTargetAnchor();
      }
    },
    // confirmIntervention(selection) {
    //   if (!this.interventionSet){
    //     // console.log("Confirmed intervention: %s", selection);
    //     this.selections['Intervention'] = selection;
    //     this.interventionSet = true;
    //   }
    // },
    // confirmDataType(selection) {
    //   if (!this.inputTypeSet){
    //       // console.log("Confirmed data type: %s", selection);
    //       this.selections['DataType'] = selection;
    //       this.myTargetURL = this.urlTargets[this.selections['Condition']][selection]
    //       this.setTargetAnchor();
    //       // console.log("Now targeting download/upload URLs of", this.myTargetURL);
    //       this.inputTypeSet = true;
    //     }
    // },
    unconfirmCondition(condition) {
      switch (condition) {
        case 'condition':
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
