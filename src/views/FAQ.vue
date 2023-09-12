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
              <v-card-title class="title text-center font-weight-bold center">
              Frequently Asked Questions
              </v-card-title>
            </v-card>
          </div>
        </div>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

  <v-container>
 
    <v-row>
      <v-col>
        
        <v-card-title class="title text-left font-weight-bold">
          How can I upload clinical reports to PredictMod?
        </v-card-title>
        <v-card-text class="text-left">
          Upon selecting the EHR or Metagenomic data model, you will be directed to the upload screen. 
          On this screen, there is a downloadable template wherein each column name corresponds to a 
          specific data field (for EHR) or bacteria strain (for Metagenomic). Additionally, there’s a 
          provided sample file containing test data which can be uploaded to experiment using PredictMod.
          For additional help with uploading and formatting data, please contact our team.
        </v-card-text >
        <v-card-title class="title text-left font-weight-bold">
          What are the possible outcomes from running PredictMod?
        </v-card-title>
        <v-card-text class="text-left">
          PredictMod will provide a prediction categorized as either “Responder” or “Non-Responder”. A “Responder” prediction 
          indicates that, according to the patient’s Electronic Health Record (EHR) or Metagenomic data, there is a higher 
          likelihood of a positive response to the specified intervention. Conversely, a “Non-Responder” prediction 
          suggests that, based on the analyzed data, the patient’s positive response to the intervention is unlikely, and 
          there is a potential for the disease to continue progressing.
        </v-card-text>
        <v-card-title class="title text-left font-weight-bold">
          Will the system store patient data?
        </v-card-title>
        <v-card-text class="text-left">
          PredictMod will use uploaded patient data to make a one-time prediction. The data will not be saved in the system.
        </v-card-text>

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

export default {

  name: 'Home',
  data() {
			return {
				home: false,
			}
    },
  components: { DisclaimerShow, LicenseShow }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
/* :gradient="linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.75))" */
#intro-img {
  background-image: linear-gradient(to bottom, rgba(119, 119, 119, 0), rgb(0, 0, 0));
}
</style>