<template>
  <v-banner
  single-line
  class="text-left">
    <v-img
      src="../assets/Welcome_Header.jpg"
      id="intro-img"
      :height="400" 
      :cover="true"
      >
      <v-card-title class="title text-center font-weight-bold">
        PredictMod
      </v-card-title>
      <v-card-text class="text-center">
        A Machine Learning-Based Application for Informed Clinical Decision Making
      </v-card-text>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

  <v-container>


    <v-row>
      <v-col>
        
        <v-card-title class="title text-left font-weight-bold">
          About PredictMod
        </v-card-title>
        <v-card-text class="text-left">
          PredictMod is an application designed to predict the outcome of an intervention prior to
          a patient initiating treatment. This application prototype employs machine learning algorithms 
          to predict whether a patient with pre-diabetes is likely to respond favorably to a diet 
          intervention and not progress to diabetes at the end of the study period. 
        </v-card-text >
        <v-card-title class="title text-left font-weight-bold">
          About HIVE Lab
        </v-card-title>
        <v-card-text class="text-left">
          HIVE Lab is involved in developing bioinformatics tools and resources, such as standards 
          for bioinformatics communication, knowledgebases for glycoinformatics 
          and infectious diseases, cancer research, and microbiome analysis.
        </v-card-text>
        <a href='https://hivelab.biochemistry.gwu.edu'>
          <v-img src='../assets/HIVELab_Logo.png' height="15%" width="15%" inline />
        </a>
        <v-card-title class="title text-left font-weight-bold">
          <a href='https://hivelab.biochemistry.gwu.edu'>
            Visit us at the HIVE Lab Website
          </a>
        </v-card-title>
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