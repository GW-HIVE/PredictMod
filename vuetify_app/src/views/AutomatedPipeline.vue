<template>
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
              Automated Pipeline Application
            </v-card-title>
            <v-card-text class="text-center">
              Bring your own data to the PredictMod AI/ML sandbox
            </v-card-text>
            </v-card>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
      </div>
      </div>
    </v-img>
  </v-banner>

  <v-container>

  <!-- <v-container :key="action">
    Current key: {{ action }}
  </v-container> -->
  <v-row>
    <v-col cols="3">
      <v-radio-group v-model="action">
        <v-radio label="Train new models" value="training"></v-radio>
        <v-radio label="New sample with your models" value="newSamplePersonal"></v-radio>
        <v-radio label="New sample with shared models" value="newSampleShared"></v-radio>
      </v-radio-group>
    <!-- <v-card flat :key="action" v-if="action === 'newSample'">
      <v-card-title>Your models</v-card-title>
      <v-list style="max-height: 500px" class="overflow-y-auto">
        <v-list-item
          v-for="obj in availableModels"
          :key="obj.model_name"
        >
        <v-card class="text-left" variant="outlined" hover style="border: 1px solid lightgrey">
          <v-card-title>{{ obj.model_name }}
          </v-card-title>
          <v-card-text>{{ obj.id }}</v-card-text>
            <v-row><v-btn variant="flat" onclick="alert('Moar')">More details</v-btn>
            <v-btn variant="flat" onclick="alert('delete!')">Delete</v-btn>
          </v-row>
        </v-card>
      </v-list-item>
    </v-list>
    </v-card> -->
  </v-col>
  <v-col cols="9">
    <v-row>
      <v-col>
        <AutomatedPipelineUpload 
          v-if="action == 'training'"
          :upload-target-u-r-l="'pipeline'"
        />
        <AutomatedPipelineReuseModels
          v-if="action == 'newSamplePersonal'"
          :upload-target-u-r-l="'pipeline'"
          :models-u-r-l="'user-models/'" 
        />
        <AutomatedPipelineSharedModels
          v-if="action == 'newSampleShared'"
          :upload-target-u-r-l="'pipeline'"
          :models-u-r-l="'user-models/'" 
        />
      </v-col>
    </v-row>
  </v-col>
</v-row>

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


</template>
<script>
import { onMounted, ref } from 'vue';

import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import LicenseShow from './LicenseShow.vue';
import AutomatedPipelineUpload from '@/components/AutomatedPipelineUpload.vue';
import AutomatedPipelineReuseModels from './AutomatedPipelineReuseModels.vue';
import AutomatedPipelineSharedModels from './AutomatedPipelineSharedModels.vue';

export default {

  name: 'Home',
  data() {
			return {
				home: false,
        action: "training",
			}
    },
  components: { DisclaimerShow, LicenseShow, AutomatedPipelineUpload, AutomatedPipelineReuseModels, AutomatedPipelineSharedModels }
}
</script>
