<template>
  <!-- <v-banner
  single-line
  class="text-left"> -->
  <v-card>
    <v-img
      src="../assets/Welcome_Header.jpg"
      id="intro-img"
      gradient="to bottom, rgba(119, 119, 119, 0.25), rgba(0, 0, 0, 0.75)"
      :height="400" 
      :cover="true"
      >
      <!-- <v-overlay absolute> -->
      <!-- 
        See below for the (currently...) most reliable overview of v-img
        use cases. 
        https://codingbeautydev.com/blog/vuetify-image/?expand_article=1
        NB: `:gradient` is broken as of vuetify ^3.0.0, `gradient="xxx"`
        must be used.
       -->
       
        <div class="d-flex fill-height" style="flex-direction:column">
          <div class="d-flex fill-height align-center justify-center"> 
     
          <v-card flat color="transparent">
            <v-card-title class="title text-center font-weight-bold">
              Welcome to PredictMod (beta)
            </v-card-title>
            <v-card-text class="text-center">
              Welcome to PredictMod! PredictMod is a machine-learning-based platform that predicts whether 
	      a patient will respond to an intervention based on electronic health records (EHR) or -omic data.
            </v-card-text>
         </v-card>
       
          </div>
        </div> 
     
      <!-- </v-overlay> -->
    </v-img>
  </v-card>
  <!-- </v-banner> -->

  <v-container>
 

    <v-row>
          <v-col>
            <EHRThumb/>
          </v-col>
          <v-col>
            <MGThumb/>
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

// import SimpleUploadMG from './SimpleUploadMG.vue';
// import SimpleUploadEHR from './SimpleUploadEHR.vue';
import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import EHRThumb from './EHRThumb.vue';
import MGThumb from './MGThumb.vue';
import LicenseShow from './LicenseShow.vue';

export default {

  name: 'Home',
  data() {
			return {
				home: false,
			}
    },
  components: { DisclaimerShow, NotFound, EHRThumb, MGThumb, LicenseShow }
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
