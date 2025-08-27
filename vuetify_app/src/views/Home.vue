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
      fluid
      >

        <div class="d-flex fill-height" style="flex-direction:column">
          <div class="d-flex fill-height align-center justify-center">

          <v-card flat color="transparent">
            <v-card-title class="title text-center font-weight-bold">
              <!-- <h1>Welcome to PredictMod <font size="-1">BETA</font></h1> -->
              <h1>Welcome to PredictMod</h1>
            </v-card-title>
            <v-card-text class="text-center">
              <h4>Welcome to PredictMod! PredictMod is a machine-learning-based platform that predicts whether
	      a patient will respond to an intervention based on electronic health records (EHR) or -omic data.</h4>
            </v-card-text>
            <v-card-actions class="justify-center">
        <!-- 
        <router-link to="/predictmod/help">
          <v-btn variant="tonal" color="#efefef">
            Learn More
          </v-btn>
        </router-link> 
        -->
          <v-btn variant="tonal" color="#efefef" href="https://hivelab.biochemistry.gwu.edu/wiki/PredictMod">
            Learn More
          </v-btn>
        </v-card-actions>
         </v-card>
          </div>
        </div>

    </v-img>


  </v-banner>

  <!-- <router-link to="/predictmod/testing">
    <v-btn>Testing Space</v-btn>
  </router-link> -->

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
        <v-card flat color="transparent">
          <v-card-title class="title text-center font-weight-bold">
            Explore models in the PredictMod platform
          </v-card-title>
          <v-card-text class="text-center">
            See the models that make up the PredictMod platform ecosystem
          </v-card-text>
        </v-card>
        <router-link to="/predictmod/models">
              <v-btn color="primary">Start exploring</v-btn>
        </router-link>
        <v-row>

      </v-row>
      </v-col>
    <v-col cols="5">
      <v-card outlined>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Version</h3>
        </v-card-title>
        <v-card-text class="text-center">
          User Interface v1.13 (9 July 2025)
        </v-card-text>
      </v-card>
      <v-card outlined flex>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Model Statistics</h3>
        </v-card-title>
        <ReleasedModels :data="this.appStore.releasedModels" v-if="show_models" />

      </v-card>
      <!-- <v-card outlined>
        <v-card-title class="title text-center font-weight-bold">
          <h3>Anticipated Future Models</h3>
        </v-card-title>
        <PendingModels :data="this.appStore.pendingModels" v-if="show_models" />
      </v-card> -->
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
import ReleasedModels from '@/components/ReleasedModels.vue';
import PendingModels from '@/components/PendingModels.vue';
import { useAppStore } from '@/store/app';
import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import LicenseShow from './LicenseShow.vue';

import axios from "axios";

export default {

  name: 'Home',
  data() {
			return {
				home: false,
        releasedModels: null,
        pendingModels: null,
        show_models: false,
			}
    },
  setup() {
    const appStore = useAppStore();
    return { appStore };
  },
  mounted() {
    this.getModels();
  },
  methods: {
    alertTBD(source) {
      alert(source + " functionality is under development");
    },
    async getModels() {
      this.appStore.getModels();
      this.show_models = true;
    },
  },
  components: { ReleasedModels, PendingModels, DisclaimerShow, NotFound, LicenseShow },
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
