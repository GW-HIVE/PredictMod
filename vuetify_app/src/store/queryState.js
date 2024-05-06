import { defineStore } from "pinia";

export const useQueryState = defineStore("query", {
  state: () => ({
    condition: null,
    intervention: null,
    datatype: null,
    filePreviewData: null,
    downloadDrawer: false,
    // conditionSet: false,
    // interventionSet: false,
    // inputTypeSet: false,
    // home: false,
    interventionOptions: [],
    dataTypeOptions: [],
    // selections: {},
    targetURL: "",
    modelAnchor: "",    
    // targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api' : '/predictmod/api',

    conditions: [  // Ideally, populated once after mounting
      {
        name: "Prediabetes",
        description: `A precursor to Type 2 Diabetes Mellitus (T2DM), where blood sugars are higher than normal, 
        but not high enough to be considered T2DM. Prediction outcomes are based 
        on a 5% reduction in weight, HOMA-IR, or a diagnosis of T2DM.`
      },
      {
        name: "Epilepsy",
        description: 
            `A neurological disorder in which nerve cell activity in the brain 
            is disturbed, causing seizures. Prediction outcomes are based on [TBD].`
      },
      {
        name: "Renal Carcinoma",
        description: `[TBD]`,
      },
    ],
    interventions: { // Populated based on selection of 'conditions'
      'Prediabetes':
      [
        {name: "Diet - Dietary Counseling", description: "Involves following a physician-recommended diet for the management of prediabetes."},
        {name: "Diet - Keto Diet", description: "A low-carb, ketogenic diet commonly recommended for the management of prediabetes."},
        {name: "Exercise", description: "Involves following a physician-recommended exercise regimen for the management of prediabetes."},
        {name: "Medication - Semaglutide", description: "Medication management of prediabetes using an increasingly popular GLP1-agonist."},
        {name: "No Intervention", description: "Predictions based on existing biomarkers. These predictions do not involve a specific intervention."},
      ],
    'Epilepsy':
    [
      {name: "TBD", description: "TBD"},
    ],
    'Renal Carcinoma':
    [
      {name: "TBD", description: "TBD"},
    ],
    },
    urlTargets: {  // Populated based on selection of 'conditions'
      "Prediabetes": 
      {
        "EHR": "ehr",
        "Gut Microbiome": "mg",
      },
    "Epilepsy": {},
    "Renal Carcinoma": {},
    },
    dataInputTypes: {  // Populated based on selection of 'conditions'
      'Prediabetes': 
      [
        {name: "EHR", description: "Data sourced from clinical Electronic Health Records ,e.g. EPIC-COSMOS or MDClone"},
        {name: "Gut Microbiome", description: "Microflora population and diversity information measured via High Throughput Sequencing"},
        {name: "Glycoproteomics", description: "TBD"},
        {name: "Glycomics", description: "TBD"},
      ],
     'Epilepsy':
      [
        {name: "TBD", description: "TBD"},
      ],
      'Renal Carcinoma':
    [
      {name: "TBD", description: "TBD"},
    ],
    },

  }),

  mounted() {
  },

  getters: { /* */ },
  actions: {

    populateOptions() {
      // TODO: Reach out over backend API to retrieve 'condition' options
    },

    confirmCondition() {},

    confirmIntervention() {},

    confirmDataType() {},

    getMenuSelection(selectionString) {
      // console.log('---> Checking for state ' + selectionString);
      // console.log('Available states: %s | %s | %s', this.condition, this.intervention, this.datatype);
      switch(selectionString) {
        case 'condition':
          return this.condition;
        case 'intervention':
          return this.intervention;
        case 'datatype':
          return this.datatype;
        default:
          return null;
      }
    },

    getConditions() {
      return this.conditions;
    },

    populateConditionOptions() {
      // TODO: API call to retrieve information from backend
      // console.log("Now retrieving options based on condition: %s", this.condition);
      if (this.condition !== null) {
        this.interventionOptions = this.interventions[this.condition];
        this.dataTypeOptions = this.dataInputTypes[this.condition];
      }
    },

    registerURL() {
      // console.log("Condition: %s | Intervention: %s | Data Type: %s", this.condition, this.intervention, this.datatype);
      if (
        this.condition !== null &&
        this.intervention !== null &&
        this.datatype !== null
      ) {
        this.targetURL = this.urlTargets[this.condition][this.datatype];
        // console.log("---> Found target URL %s", this.targetURL)
      } else {
        this.targetURL = "";
      }
    },

    resetState() {
      console.log("Query store: Resetting state");
      this.condition = null;
      this.intervention = null;
      this.datatype = null;
      this.filePreviewData = null;
      this.downloadDrawer = false;
    },

    setState(state, stateString) {
      // console.log("Query State: Setting %s to %s", state, stateString);
      this[state] = stateString;
      if (state == "condition") {
        this.populateConditionOptions();
      }
    },
    
    setTargetAnchor() {
      if (!this.targetURL) {
        this.modelAnchor = "";
        return;
      }
      const baseString = "/predictmod/help#current-models"
      switch (this.targetURL) {
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


    clearError() {
      this.error = null;
    },

  },
});
