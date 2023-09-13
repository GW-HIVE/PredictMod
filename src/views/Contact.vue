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
        Contact Us
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
