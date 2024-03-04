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
              <h1>
                Help
              </h1>
            </v-card-title>
            <!-- <v-card-text class="text-center">
              A Machine Learning-Based Application for Informed Clinical Decision Making
            </v-card-text> -->
            </v-card>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
      </div>
      </div>
    </v-img>
  </v-banner>

  <v-container>

    <div class="title justify-center">
      <h1>Table of Contents</h1>
    </div>
    <v-row>
      <v-col>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            What is Predictmod?
          </v-card-title>
        <v-card-text>
          <router-link to="/predictmod/about">
            About Us<br>
          </router-link>
          <router-link to="/predictmod/faq">
            Frequently Asked Questions (FAQ)<br>
          </router-link>
          <router-link to="/predictmod/contact">
            Contact Us<br>
          </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Login & Registration
          </v-card-title>
        <v-card-text>
          <router-link to="/predictmod/not-found">
          How to register with PredictMod<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          Login & Registration FAQs<br>
        </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            "Try It Out" Query Builder
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/not-found">
            How the example query builder works<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          Download example data<br>
        </router-link>
        <router-link to="/predictmod/not-found">
        </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Current Models
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/not-found">
            MG_Exercise_v1.1<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          MDClone_Diet_Counseling_v1.1<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          EHR_Keto_v1.0<br>
        </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Anticipated Models<br>
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/not-found">
            Glycomics_PreDM_v1.0<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          Epilepsy_Keto_v1.1<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          Synthea_Exercise_v1.1<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          MDClone_Diet_Counseling_v1.2<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          MDClone_Semaglutide_v1.0<br>
        </router-link>
        <router-link to="/predictmod/not-found">
          MDClone_Exercise_v1.0<br>
        </router-link>
        </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Query Builder
          </v-card-title>
        <v-card-text>
          <router-link to="/predictmod/not-found">
            How the Query Builder works<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Step 1: Selecting a condition<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the Prediabetes condition<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Step 2: Selecting an intervention<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the Exercise condition<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the <i>Diet - Keto Diet</i> intervention<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the <i>Diet - Dietary Counseling</i> intervention<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Step 3: Selecting a Data Type<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the <i>Gut Microbiome</i> data type<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            About the <i>Electronic Health Records</i> data type<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Step 4: Uploading a data file<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Formatting data FAQs<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Run a prediction<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Interpreting a prediction result<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            "Responder" vs "Non-responder" outcomes<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Data visualization examples and interpretations<br>
          </router-link>
          <router-link to="/predictmod/not-found">
            Run another prediction<br>
          </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Coming soon: Upload a Model
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/not-found">
            Uploading your machine-learning model
          </router-link>
          <router-link to="/predictmod/not-found">
            Model review & verification process
          </router-link>
          <router-link to="/predictmod/not-found">
            Model Upload FAQs
          </router-link>
        </v-card-text>
        </v-card>
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
