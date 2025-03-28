<template>
  <v-container fluid>
    <!-- 
    Models to toggle: {{ modelsToShare.toString() }}
    Models to use: {{ modelsToUse.toString() }} 
    -->
  <v-card flat>
    <v-card-title>Shared models</v-card-title>
    <v-card v-if="availableDataTypes.length == 0" :key="availableDataTypes">
      No shared models found
    </v-card>
    <v-row dense>
    <v-col md="5" class="d-flex pa-0 h-25" dense>
      <v-list 
        style="max-height: 500px" 
        class="overflow-y-auto" 
        v-if="availableDataTypes.length > 0"
        :key="availableDataTypes"
      >
      <v-list-item
        v-for="obj in availableDataTypes"
        :key="availableDataTypes"
        v-model="selectedDataType"
      >
      <v-card 
        class="text-left pa-0" 
        variant="outlined" 
        style="border: 1px solid lightgrey"
        fluid
      >
        <v-row>
        <v-card-title>
          {{ padName(obj.name) }}
        </v-card-title>
      </v-row>
        <!-- <v-row>
          <v-card-text>TBD</v-card-text>
        </v-row> -->
        <!-- <v-row class="align-left"> -->
            <v-card-actions>
            <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="getModels(obj.name)">
              {{ selectedDataType == obj.name ? "Deselect  " : "Select" }}
            </v-btn>
            <!-- <v-btn variant="flat" class="pa-2 ma-0" onclick="alert('Moar')">More details</v-btn> -->
            <!-- <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="deleteClicked.push(obj.name)">Delete</v-btn> -->
          </v-card-actions>
        <!-- </v-row> -->
        <!-- <v-expand-transition>
          <v-alert
            v-if="deleteClicked.includes(obj.name)"
            class="position-absolute w-100"
            height="100%"
            style="bottom: 0;"
            type="warning"
            density="compact"
            closable
            @click.close="deleteClicked.splice(deleteClicked.indexOf(obj.name), 1)"
          >
          <v-alert-text @click.prevent="deleteFamily(obj.name)" hover>
            Warning - Confirm? 
          </v-alert-text>
          <v-btn size="small" block @click.prevent="deleteFamily(obj.name)" variant="outlined">Confirm?</v-btn>
          </v-alert>
        </v-expand-transition> -->
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
        <v-card-title>{{ obj.model_name + ": (Trained on " + obj.created + ")" }}
        </v-card-title>
        <!-- <v-card-text>{{ obj.model_name + ":" + obj.id }}</v-card-text> -->
        <v-card-actions>
        <div>
          <v-row>
            <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="tbd">More details</v-btn>
            <!-- <v-btn variant="flat" class="pa-2 ma-0" @click.prevent="deleteClicked.push(obj.id)">Delete</v-btn> -->
          </v-row>  
          <!-- <v-layout class="pa-0" dense> -->
            <!-- align="center" justify="center"  -->
          <v-row d-flex nowrap class="align-left px-0 ma-0">
            <!-- :label="`${getSaveString(obj)}`" -->
            <!-- <v-checkbox
            v-model="modelsToShare"
            class="shrink pa-0 ma-0"
            :label="`${obj.allUserShared ? 'Make model private' : 'Share model with all users'}`"
            :value="obj.id"
            :messages="`${getSaveString(obj)}`"
          ></v-checkbox> -->
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
          density="compact"
          closeable
          @click.close="deleteClicked.splice(deleteClicked.indexOf(obj.id), 1)"
        >
        <v-alert-title>
          Warning - this cannot be undone. 
        </v-alert-title>
        <v-btn @click.prevent="deleteModel(obj.id);" variant="outlined">Confirm?</v-btn>
        </v-alert>
      </v-expand-transition>
      </v-card>
    </v-list-item>
    </v-list>
  </v-col>
  </v-row>
  <v-card variant="flat" v-slot:actions>
    <!-- <v-btn
      @click="submitShares" 
      color="primary"
      variant="flat"
    >
    Submit model shares
  </v-btn> -->
  <v-btn 
      @click="sumbitModelsForUse"
      color="primary"
      variant="flat"
    >
    {{ modelsToShare.length == 0 ? 'Use selected models' : 'Submit selected shares and use selected models' }}
  </v-btn>
  <v-btn @click.submit="clearResults" color="primary" variant="flat">Clear previous results</v-btn>
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
      label="Select a new sample to use (csv, tsv, xlsx, xls)"
      type="File"
      v-model="currentFile"
    ></v-file-input>
    <!-- </v-row> -->
  </div>
</v-card>
</v-container>
<v-container>
  <v-row class="pa-5" v-if="response">
        <PipelineResultsCard 
          :data="response"
        />
    </v-row>
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
  components: { PipelineResultsCard, UploadService },
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
      modelsToShare: [],
      modelsToUse: [],
      deleteClicked: [],
    }
  },
  methods: {
    clearError() {
      this.error = ""
    },
    padName(name) {
      if (name.length < 25) {
        return (name + "                         ").substring(0, 25)
      } else {
        return name
      }
    },
    tbd() {alert("TBD")},
    clearResults() {
      this.response = null
    },
    async deleteModel(modelID) {
      const modelsURL = this.baseURL + "/" + `${this.modelsURL}?action=delete_model&model_id=${modelID}&target=pipeline`
      console.log("---> Called get models. Collecting from " + modelsURL)
      const response = await fetch(modelsURL, {
          credentials: "include",
        })
      const result = await response.json()
      console.log("Deleting model: Found response " + JSON.stringify(result))
      this.getModels()
      this.deleteClicked.splice(this.deleteClicked.indexOf(modelID), 1);
    },
    async deleteFamily(modelFamilyName) {
      alert("Now deleting family of models: " + modelFamilyName)
      const modelsURL = this.baseURL + '/' + this.modelsURL + `?action=delete_model_family&data_type=${modelFamilyName}&target=pipeline`
      console.log("---> Called get models. Collecting from " + modelsURL)
      const response = await fetch(modelsURL, {
          credentials: "include",
        })
      const deletedFamilyResponse = await response.json()
      console.log("Got deleted family response " + JSON.stringify(deletedFamilyResponse))
      this.availableDataTypes = this.availableDataTypes.filter((adt) => {
        console.log("Filtering name: " + adt.name + " by filter " + JSON.stringify(deletedFamilyResponse))
        return adt.name !== deletedFamilyResponse
      })
      this.getDataTypes()
      this.getModels()
      this.deleteClicked.splice(this.deleteClicked.indexOf(deletedFamilyResponse), 1);
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
      const modelsURL = this.baseURL + '/' + this.modelsURL + "?q=data_types&shared=True"
      const response = await fetch(modelsURL, {
        credentials: "include",
      })
      const adt = await response.json()
      console.log("Got response ", typeof(adt), "-->\n", JSON.stringify(adt))

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
      const modelsURL = this.baseURL + '/' + this.modelsURL + `?data_type=${dataTypeName}&shared=True`
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
            console.log("Model: " + JSON.stringify(model))
            const createdDate = new Date(model.created)
            const updatedDate = new Date(model.updated)
            // console.log("Date: " + date + " (type " + typeof(date) + ")")
            return {
              "model_name": model.model_name,
              "id": model.id,
              "created": createdDate.toLocaleDateString("en-US", options),
              "updated": updatedDate.toLocaleDateString("en-US", options),
              "save": model.to_save ? true : false,
              "allUserShared": model.all_user_shared ? true : false,
            }
          })
      }
    },
    // async submitShares() {
    //   if (this.modelsToShare.length == 0) {
    //     alert("No models selected to adjust sharing feature")
    //   } else {
    //     const toggledModelIDs = [];
    //     this.availableModels.forEach((model) => {
    //       if (this.modelsToShare.includes(model.id)) {
    //         model.allUserShared = !model.allUserShared
    //         toggledModelIDs.push(model)
    //       }
    //     })
        
    //     const modelsURL = this.baseURL + '/update-models/?q=model_updates'
    //     const response = await fetch(modelsURL, {
    //       headers: new Headers({"X-CSRFToken": this.userStore.token}),
    //       method: 'POST',
    //       credentials: "include",
    //       body: JSON.stringify(toggledModelIDs),
    //     })

    //     if(!response.ok) {
    //       // Error handling
    //     } else {
    //       const modelsToUpdate = await response.json()
    //       this.availableModels.forEach((m) => {
    //         if (m.id in modelsToUpdate) {
    //           m = modelsToUpdate[m.id];
    //         }
    //       })
    //       this.modelsToShare = [];
    //     }
    //   }
    // },
    async sumbitModelsForUse() {
      // if (this.modelsToShare.length > 0){ 
      //   console.log("First saving selected models")
      //   this.submitShares()
      // }
      // console.log("Submitting data to the following models")
      // this.modelsToUse.forEach((m) => {
      //   console.log("Submitting model ---> ", m)
      // })
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
            this.uploadSuccess = this.upload();
        },
  
      upload() {
        if (!this.currentFile) {
          this.message = null;
          this.error = "Please select a file for upload!";
          return false;
        }
  
        this.error = null

        // Create a "Model Name" + IDs object for shipping...
        // const models = { data_name: this.selectedDataType, ids: [] }

        // this.modelsToUse.forEach((m) => {
        //   models.ids.push(m)
        // })
        // XXX
        // console.log("DataTypeName: " + this.selectedDataType)
        // console.log("Uploading to target URL: " + this.uploadTargetURL)
        // console.log("Sending models information: " + JSON.stringify(models))

        // TODO: Axios progress on upload
        // const onProgressBar = (event) => {
        //   this.progress = Math.round((100 * event.loaded) / event.total);
        // }

        const ids = []
        this.modelsToUse.forEach((m) => ids.push(m))

        UploadService.upload(this.currentFile, this.uploadTargetURL, {}, {
          action: "newSample",
          labelColumn: this.labelColumn,
          columnsToDrop: this.columnsToDrop,
          modelName: this.selectedDataType,
          modelIDs: ids,
        })
          .then((response) => {
            // this.message = response.data.message;
            // console.log("Got response:\n", response);
            if (response.networkError) {
              this.message = null
              this.error = "Error on upload: Response code " + response.error
              return false
            }
            this.message = response.result ? response.result : "Successfully uploaded";
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