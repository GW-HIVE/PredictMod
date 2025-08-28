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
    targetURLs: [],
    modelName: "",    
    // targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api' : '/predictmod/api',
    queriesURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE: "/predictmod/",
    conditions: [],
    interventions: [],
    dataTypeOptions: [],
  }),

  mounted() {
    this.populateOptions();
  },

  getters: { /* */ },
  actions: {

    async populateOptions() {
      const response = await fetch(this.queriesURL+"/api/query-conditions/");
      const result = JSON.parse(await response.json());
      // console.log("Got options ", result);
      this.conditions = [];
      result.forEach(r => {
        this.conditions.push({ name: r.fields.name, description: r.fields.description })
      });
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

    async populateConditionOptions() {
      // TODO: API call to retrieve information from backend
      // console.log("Now retrieving options based on condition: %s", this.condition);
      // if (this.condition !== null) {
      //   this.interventionOptions = this.interventions[this.condition];
      //   this.dataTypeOptions = this.dataInputTypes[this.condition];
      // }
      if (!this.condition) {
        // console.log("Found falsey condition " + this.condition + ": returning")
        return
      }
      const iResponse = await fetch(this.queriesURL+`/api/query-interventions/?c=${this.condition}`);
      const interventions = JSON.parse(await iResponse.json());
      // console.log("New interventions: ", interventions);
      // Reset state
      this.interventions = [];
      interventions.forEach(i => {
        this.interventions.push({ name: i.fields.name, description: i.fields.description })
      })
      const dtResponse = await fetch(this.queriesURL+`/api/query-input-data/?c=${this.condition}`);
      const inputDataTypes = JSON.parse(await dtResponse.json());
      // Reset state
      // console.log("New data types: ", inputDataTypes);
      this.dataTypeOptions = [];
      inputDataTypes.forEach(dt => {
        this.dataTypeOptions.push({ name: dt.fields.name, description: dt.fields.description })
      })
    },

    async registerURL() {
      // console.log("Condition: %s | Intervention: %s | Data Type: %s", this.condition, this.intervention, this.datatype);
      if (
        this.condition !== null &&
        this.intervention !== null &&
        this.datatype !== null
      ) {
        // this.targetURL = this.urlTargets[this.condition][this.datatype];
        this.targetURLs = [];
        const response = await fetch(this.queriesURL+`/api/query-model-endpoints/?c=${this.condition}&i=${this.intervention}&dt=${this.datatype}`);
        const endpoints = JSON.parse(await response.json());
        // console.log("Got response: ", JSON.stringify(endpoints));
        endpoints.forEach(model => {
          this.targetURLs.push({name: model.fields.name, link: model.fields.link});
        });
        this.targetURL = this.targetURLs[0];
        // console.log("---> Found target URL: ", JSON.stringify(this.targetURL))
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
    
    // setTargetAnchor() {
    //   if (!this.targetURL) {
    //     this.modelAnchor = "";
    //     return;
    //   }
    //   const baseString = "/predictmod/help#current-models"
    //   switch (this.targetURL) {
    //       case "mg":
    //           this.modelAnchor = baseString + "-mg-exercise";
    //           break;
    //       case "ehr":
    //           this.modelAnchor = baseString + "-ehr-diet-counseling";
    //           break;
    //       default:
    //           this.modelAnchor = "/predictmod/NotFound";
    //     }
    // },


    clearError() {
      this.error = null;
    },

  },
});
