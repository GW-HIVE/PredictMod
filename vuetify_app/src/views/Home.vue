<template>
  <v-card>
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
              Welcome to PredictMod <font size="-1">BETA</font>
            </v-card-title>
            <v-card-text class="text-center">
              Welcome to PredictMod! PredictMod is a machine-learning-based platform that predicts whether 
	      a patient will respond to an intervention based on electronic health records (EHR) or -omic data.
            </v-card-text>
         </v-card>
       
          </div>
        </div>
     
    </v-img>
  </v-card>

  <v-container>
 

    <!-- <v-row> -->
      <v-col>
        <v-card flat color="transparent">
          <v-card-title class="title text-center font-weight-bold">
            Registered User
          </v-card-title>
          <v-card-text class="text-center">
            Login to buildyour own query and run predictions with single-patient data
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/login">
              <v-btn color="primary">Login</v-btn>
        </router-link>
        <v-card flat color="transparent">
          <v-card-title class="title text-center font-weight-bold">
            Explore our models?
          </v-card-title>
          <v-card-text class="text-center">
            Review, interact and learn about the PredictMod model collection.
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/explore">
              <v-btn color="primary">Explore</v-btn>
        </router-link>
        <v-card flat color="transparent">
          <v-card-title class="title text-center font-weight-bold">
            Guest User
          </v-card-title>
          <v-card-text class="text-center">
            Run a sample query to see how the PredictMod tool works
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/try-it">
              <v-btn color="primary">Get Started</v-btn>
        </router-link>
      </v-col>

    <!-- </v-row> -->
  

    <v-row>
      <v-col>
          <DisclaimerShow/>
      </v-col>
      <v-col>
        <LicenseShow/>
      </v-col>
    </v-row>


</v-container>

</template>
<script>
import { onMounted, ref } from 'vue';

// import SimpleUploadMG from './SimpleUploadMG.vue';
// import SimpleUploadEHR from './SimpleUploadEHR.vue';
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
  components: { DisclaimerShow, NotFound, LicenseShow }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
#intro-img {
  color: #fcfcfc;
}
/* :gradient="linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.75))" */
/*
Broken css: 
#intro-img {
  background-image: linear-gradient(to bottom, rgba(119, 119, 119, 0), rgb(0, 0, 0));
}
*/
</style>
