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
        Contact Us
      </v-card-title>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

  <v-container>


    <v-row>
      <v-col>

        <v-card-title class="title text-left font-weight-bold">
          Send a Message          
        </v-card-title>
        <v-card-text class="text-left">
          We always welcome questions, comments, and suggestions regarding our website. 
          We will make every effort to respond to you within a reasonable amount of time. 
          Email us at <a href="mailto:mazumder_lab@gwu.edu">mazumder_lab@gwu.edu</a>.
        </v-card-text >
        <v-card-title class="title text-left font-weight-bold">
          GW Location
        </v-card-title>
        <v-card-text class="text-left">
          The George Washington University
          School of Medicine and Health Sciences
          2300 Eye Street N.W.,
          Washington, DC 20037
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