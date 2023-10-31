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
        Clinician and Researcher Access
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

        <v-card-title class="title text-center font-weight-bold">
          Login or register for access to PredictMod          
        </v-card-title>
        <v-card-text class="text-center">
            We endeavor to enable user login shortly!
        </v-card-text >
      </v-col>
    
    </v-row>

    <v-container>
    <v-row class="justify-center">
      <v-card-title class="title text-center font-weight-bold" >
        <v-btn @click.prevent="tbdAlert()">
          Login
          <!-- Unclear if this is needed in v-btn: href="/predictmod/admin/login/" -->
        </v-btn>
        <v-btn @click.prevent="tbdAlert()">
          <!-- Unclear if this is needed in v-btn: href="/predictmod/admin/register/" -->
          Register
        </v-btn>
      </v-card-title>
    </v-row>
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
  components: { DisclaimerShow, LicenseShow },
  methods:
    {
      tbdAlert () {
            // Depending on how we proceed, see here for download support:
            // https://stackoverflow.com/questions/53772331/vue-html-js-how-to-download-a-file-to-browser-using-the-download-tag
            //
            alert("Login facilities are under development");
            console.log("---> Login facilities are under development");
        },
    }
}
</script>
