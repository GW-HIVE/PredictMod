<template>
  <v-container fluid>
    Models to toggle: {{ modelsToSave.toString() }}
    Models to use: {{ modelsToUse.toString() }}
  <v-card flat>
    <v-card-title>Your models</v-card-title>
    <v-card v-if="availableDataTypes.length == 0">
      No models found
    </v-card>
    <v-row dense>
    <v-col md="5" class="d-flex pa-0 h-25" dense>
      <v-list 
        style="max-height: 500px" 
        class="overflow-y-auto" 
        v-if="availableDataTypes.length > 0"
      >
      <v-list-item
        v-for="obj in availableDataTypes"
        :key="obj.name"
        v-model="selectedDataType"
      >
      <v-card 
        class="text-left pa-0" 
        variant="outlined" 
        style="border: 1px solid lightgrey"
        dense
      >
        <v-row>
        <v-card-title>
          {{ obj.name }}
        </v-card-title>
      </v-row>
        <!-- <v-row>
          <v-card-text>TBD</v-card-text>
        </v-row> -->
        <!-- <v-row class="align-left"> -->
          <template v-slot:actions>
            <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="getModels(obj.name)">
              {{ selectedDataType == obj.name ? "Deselect  " : "Select" }}
            </v-btn>
            <!-- <v-btn variant="flat" class="pa-2 ma-0" onclick="alert('Moar')">More details</v-btn> -->
            <v-btn variant="flat" class="pa-2 ma-0" onclick="alert('delete!')">Delete</v-btn>
          </template>
        <!-- </v-row> -->
      </v-card>
    </v-list-item>
    </v-list>
    </v-col>
    <v-col width="9" align="center" md="7" dense>
    <v-list 
      style="max-height: 500px" 
      class="overflow-y-auto" 
      v-if="availableModels.length > 0"
    >
      <v-list-item
        v-for="obj in availableModels"
        :key="obj.model_name"
      >
      <v-card class="text-left mx-auto" variant="outlined" hover style="border: 1px solid lightgrey">
        <v-card-title>{{ obj.model_name + ": " + obj.id + " (Trained at " + obj.created + ")" }}
        </v-card-title>
        <!-- <v-card-text>{{ obj.model_name + ":" + obj.id }}</v-card-text> -->
        <v-card-actions>
        <div>
          <v-row>
            <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="tbd">More details</v-btn>
            <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="deleteClicked.push(obj.id)">Delete</v-btn>
          </v-row>  
          <!-- <v-layout class="pa-0" dense> -->
            <!-- align="center" justify="center"  -->
          <v-row d-flex nowrap class="align-left px-0 ma-0">
            <!-- :label="`${getSaveString(obj)}`" -->
            <v-checkbox
            v-model="modelsToSave"
            class="shrink pa-0 ma-0"
            :label="`${obj.save ? 'Mark for removal' : 'Save model'}`"
            :value="obj.id"
            :messages="`${getSaveString(obj)}`"
          ></v-checkbox>
          <v-checkbox
            label="Use model"
            v-model="modelsToUse"
            class="shrink pa-0 ma-0"
            :value="obj.id"
            messages="Select to use this model on submission"
            ></v-checkbox>
          <!-- </v-layout> -->
          </v-row>
        </div>
      </v-card-actions>
      <v-expand-transition>
        <v-alert
          v-if="deleteClicked.includes(obj.id)"
          class="position-absolute w-100"
          height="100%"
          style="bottom: 0;"
          type="warning"
        >
        <v-alert-title>
          Warning - this cannot be undone. 
        </v-alert-title>
        <v-btn @click.prevent="deleteClicked.splice(deleteClicked.indexOf(obj.id), 1);" variant="outlined">Proceed?</v-btn>
        </v-alert>
      </v-expand-transition>
      </v-card>
    </v-list-item>
    </v-list>
  </v-col>
  </v-row>
  <v-card variant="flat" v-slot:actions>
    <v-btn
      @click="submitSaves" 
      color="primary"
      variant="flat"
    >
    Submit model saves
  </v-btn>
  <v-btn 
      @click="sumbitModelsForUse"
      color="primary"
      variant="flat"
    >
    {{ modelsToSave.length == 0 ? 'Use selected models' : 'Submit selected saves and use selected models' }}
  </v-btn>
  <!-- <v-row v-if="error"> -->
    <v-alert
          v-if="error"
          class="position-absolute w-100"
          height="100%"
          style="bottom: 0;"
          type="error"
        >
        <v-alert-title>
          {{ error }}
        </v-alert-title>
        <v-btn @click.submit="clearError">Clear error</v-btn>
      </v-alert>
  <!-- </v-row> -->
  </v-card>
  <div>
  <!-- <v-row class="pa-0"> -->
    <v-file-input
      show-size
      label="Select a new sample to use (xls or xlsx)"
      type="File"
      v-model="currentFile"
    ></v-file-input>
    <!-- </v-row> -->
  </div>
</v-card>
</v-container>
</template>

<script>
import PipelineResultsCard from '@/components/PipelineResultsCard.vue';
import UploadService from '@/services/UploadService';
import { useUserStore } from '@/store/user';
import * as XLSX from 'xlsx';

const options = {day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "2-digit", hour12: true}

export default {
  name: "pipeline-model-reuse",
  props: {
    uploadTargetURL: String,
    modelsURL: String,
  },
  components: {PipelineResultsCard, UploadService },
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  mounted() {
    this.getDataTypes()
  },
  data() {
    return {
      baseURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + "/api": "/predictmod/api",
      data: null,
      currentFile: null,
      response: null,
      progress: 0,
      message: "Data must be selected before results are available",
      error: null,
      uploadSuccess: false,
      availableDataTypes: [],
      availableModels: [],
      selectedDataType: "",
      modelsToSave: [],
      modelsToUse: [],
      deleteClicked: [],
    }
  },
  methods: {
    clearError() {
      this.error = ""
    },
    tbd() {alert("TBD")},
    async deleteModel(modelID) {
      const fullURL = this.baseURL + "/" + `${this.modelsURL}?q=delete_model&model_id=${modelID}`
    },
    getSaveString(obj) {
      if (obj.save) {
        return `Model is currently saved`
      } else {
        const oneDayLater = new Date(obj.updated)
        oneDayLater.setHours(oneDayLater.getHours() + 24*30)
        return `Will expire on ${oneDayLater.toLocaleDateString("us-EN", options)}`
      }
    },
    async getDataTypes() {
      // console.log("---> Data types initialization: ", typeof(this.availableDataTypes))
      const modelsURL = this.baseURL + '/' + this.modelsURL + "?q=data_types"
      const response = await fetch(modelsURL, {
        credentials: "include",
      })
      const adt = await response.json()
      // console.log("Got response ", typeof(adt), "--> ", adt)

      this.availableDataTypes = adt
      // console.log("---> Data types available: ", typeof(this.availableDataTypes))

    },
    async getModels(dataTypeName) {
      console.log("Checking for models with arg ", dataTypeName)
      if (this.selectedDataType == dataTypeName) {
          this.availableModels = [];
          this.selectedDataType = "";
          return
        }
      const modelsURL = this.baseURL + '/' + this.modelsURL + `?data_type=${dataTypeName}`
      console.log("---> Called get models. Collecting from " + modelsURL)
      const response = await fetch(modelsURL, {
          credentials: "include",
        })
      const models = await response.json()
      // console.log("Got response ", JSON.stringify(models))
      if (!response.ok) {
      // Error handling
        } else {
        this.selectedDataType = dataTypeName
        this.availableModels = Array.from(models.models_available).map((model) => {
            // console.log("Model: " + JSON.stringify(model))
            const createdDate = new Date(model.created)
            const updatedDate = new Date(model.updated)
            // console.log("Date: " + date + " (type " + typeof(date) + ")")
            return {
              "model_name": model.model_name,
              "id": model.id,
              "created": createdDate.toLocaleDateString("en-US", options),
              "updated": updatedDate.toLocaleDateString("en-US", options),
              "save": model.to_save ? true : false
            }
          })
      }
    },
    async submitSaves() {
      if (this.modelsToSave.length == 0) {
        alert("No models selected to adjust save feature")
      } else {
        const toggledModelIDs = [];
        this.availableModels.forEach((model) => {
          if (this.modelsToSave.includes(model.id)) {
            model.save = !model.save
            toggledModelIDs.push(model)
          }
        })
        
        const modelsURL = this.baseURL + '/update-models/?q=model_updates'
        const response = await fetch(modelsURL, {
          headers: new Headers({"X-CSRFToken": this.userStore.token}),
          method: 'POST',
          credentials: "include",
          body: JSON.stringify(toggledModelIDs),
        })

        if(!response.ok) {
          // Error handling
        } else {
          const modelsToUpdate = await response.json()
          this.availableModels.forEach((m) => {
            if (m.id in modelsToUpdate) {
              m = modelsToUpdate[m.id];
            }
          })
          this.modelsToSave = [];
        }
      }
    },
    async sumbitModelsForUse() {
      if (this.modelsToSave.length > 0){ 
        console.log("First saving selected models")
        this.submitSaves()
      }
      console.log("Submitting data to the following models")
      this.modelsToUse.forEach((m) => {
        console.log("Submitting model ---> ", m)
      })
      this.importFileAndScan();
      // const runningURL = this.baseURL + `/run-user-models/?q=run-samples&model_ids${}`
      // const response = await fetch(runningURL,
      //   {
      //     method: 'POST',
      //     body: { modelsToUse },
      //   }
      // )
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
  
        this.error = null

        // Create a "Model Name" + IDs object for shipping...
        const models = { data_name: this.selectedDataType, ids: [] }

        this.modelsToUse.forEach((m) => {
          models.ids.push(m)
        })
        console.log("DataTypeName: " + this.selectedDataType)
        console.log("Uploading to target URL: " + this.uploadTargetURL)
        console.log("Sending models information: " + JSON.stringify(models))

        UploadService.upload(this.data, this.uploadTargetURL, (event) => {
          this.progress = Math.round((100 * event.loaded) / event.total);
        }, this.labelColumn, this.columnsToDrop, 'newSample', models)
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