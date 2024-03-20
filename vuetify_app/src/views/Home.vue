<template>
  <v-banner
    single-line
  >
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
              <h1>Welcome to PredictMod <font size="-1">BETA</font></h1>
            </v-card-title>
            <v-card-text class="text-center">
              <h4>Welcome to PredictMod! PredictMod is a machine-learning-based platform that predicts whether 
	      a patient will respond to an intervention based on electronic health records (EHR) or -omic data.</h4>
            </v-card-text>
            <v-card-actions class="justify-center">
        <router-link to="/predictmod/help">
              <v-btn variant="tonal" color="#efefef">
        Learn More
        </v-btn>
        </router-link>
        </v-card-actions>
         </v-card>
          </div>
        </div>

    </v-img>


  </v-banner>


  <v-container>
 

    <v-row no-gutters>
      <v-col cols="7">
        <v-card flat color="transparent">
          <v-card-title class="title text-center font-weight-bold">
            Registered User
          </v-card-title>
          <v-card-text class="text-center">
            Login to build queries and run predictions with single-patient data
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/login">
              <v-btn color="primary">Login</v-btn>
        </router-link>

        <v-card flat color="transparent"> 
          <v-card-title class="title text-center font-weight-bold">
            Guest User
          </v-card-title>
          <v-card-text class="text-center">
            Run a sample query to see how the PredictMod tool works
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/query-builder">
              <v-btn color="primary">Try it out</v-btn>
        </router-link>
      </v-col>
    <v-col cols="5">
      <v-card outlined>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Version</h3>
        </v-card-title>
        <v-card-text class="text-center">
          User Interface v1.2 (29 Feb 2024)
        </v-card-text>
      </v-card>
      <v-card outlined>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Model Statistics</h3>
        </v-card-title>
        <v-card-text>
        <v-row>
        <v-col cols="6" class="text-left">
          <b>MG_Exercise</b><br>
          Release Date<br>
          Data Type<br>
          Patients<br>
          Genomes<br>
          Model Type<br>
        </v-col>
        <v-col cols="6" class="text-center">
          <b>v1.1</b><br>
          31 May 2023<br>
          Metagenomic<br>
          40<br>
          281<br>
          Decision Tree Classifier (DTC)<br>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" class="text-left ma=2 pa=2">
          <b>MDClone_Diet_Counseling</b><br>
          Release Date<br>
          Data Type<br>
          Patients<br>
          Data Features<br>
          Model Type<br>
        </v-col>
        <v-col cols="6" class="text-center">
          <b>v1.1</b><br>
          11 Dec 2023<br>
          EHR<br>
          19,842<br>
          19<br>
          Decision Tree Classifier (DTC)<br>
        </v-col>
      </v-row>
      </v-card-text>
      </v-card>
      <v-card outlined>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Anticipated Future Models</h3>
        </v-card-title>
        <v-card-text class="text-center">
          <v-row>
          <v-col cols="6" class="text-left">
            <b>Model Name</b><br>
            PredictMod_EHR_Keto<br>
            Glycomics_PreDM<br>
            Glycoproteomics_RC<br>
            Epilepsy_Keto<br>
            Synthea_Exercise<br>
            MDClone_Diet_Counseling<br>
            MDClone_Semaglutide<br>
            MDClone_Exercise<br>
          </v-col>
          <v-col cols="2" class="text-center">
            <b>Version</b><br>
            1.0<br>
            1.0<br>
            1.0<br>
            1.0<br>
            1.1<br>
            1.2<br>
            1.0<br>
            1.0<br>
          </v-col>
          <v-col cols="4" class="text-center">
            <b>Data Type</b><br>
            EHR<br>
            Glycomic<br>
            Glycoproteomic<br>
            Metagenomic<br>
            EHR<br>
            EHR<br>
            EHR<br>
            EHR<br>
          </v-col>
        </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
        


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
  methods: {
    alertTBD(source) {
      alert(source + " functionality is under development");
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
