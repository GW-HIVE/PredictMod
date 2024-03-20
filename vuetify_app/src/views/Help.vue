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
          <router-link to="/predictmod/help#how-to-register">
          How to register with PredictMod<br>
        </router-link>
        <router-link to="/predictmod/help#login-faqs">
          Login & Registration FAQs<br>
        </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            "Try It Out" Query Builder
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/help#tio-query-builder">
            How the example query builder works<br>
        </router-link>
        <router-link to="/predictmod/help#example-downloads">
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
          <router-link to="/predictmod/help#current-models">
            MG_Exercise_v1.1<br>
        </router-link>
        <router-link to="/predictmod/help#current-models">
          MDClone_Diet_Counseling_v1.1<br>
        </router-link>
        <router-link to="/predictmod/help#current-models">
          EHR_Keto_v1.0<br>
        </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Anticipated Models<br>
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/help#anticipated-models">
            Glycomics_PreDM_v1.0<br>
        </router-link>
        <router-link to="/predictmod/help#anticipated-models">
          Epilepsy_Keto_v1.1<br>
        </router-link>
        <router-link to="/predictmod/help#anticipated-models">
          Synthea_Exercise_v1.1<br>
        </router-link>
        <router-link to="/predictmod/help#anticipated-models">
          MDClone_Diet_Counseling_v1.2<br>
        </router-link>
        <router-link to="/predictmod/help#anticipated-models">
          MDClone_Semaglutide_v1.0<br>
        </router-link>
        <router-link to="/predictmod/help#anticipated-models">
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
          <router-link to="/predictmod/help#query-builder">
            How the Query Builder works<br>
          </router-link>
          <router-link to="/predictmod/help#qb-step-1">
            Step 1: Selecting a condition<br>
          </router-link>
          <router-link to="/predictmod/help#about-prediabetes">
            About the Prediabetes condition<br>
          </router-link>
          <router-link to="/predictmod/help#qb-step-2">
            Step 2: Selecting an intervention<br>
          </router-link>
          <router-link to="/predictmod/help#about-exercise">
            About the Exercise condition<br>
          </router-link>
          <router-link to="/predictmod/help#about-keto-diet">
            About the <i>Diet - Keto Diet</i> intervention<br>
          </router-link>
          <router-link to="/predictmod/help#about-diet-couseling">
            About the <i>Diet - Dietary Counseling</i> intervention<br>
          </router-link>
          <router-link to="/predictmod/help#qb-step-3">
            Step 3: Selecting a Data Type<br>
          </router-link>
          <router-link to="/predictmod/help#about-gut-microbiome">
            About the <i>Gut Microbiome</i> data type<br>
          </router-link>
          <router-link to="/predictmod/help#about-ehr">
            About the <i>Electronic Health Records</i> data type<br>
          </router-link>
          <router-link to="/predictmod/help#qb-step-4">
            Step 4: Uploading a data file<br>
          </router-link>
          <router-link to="/predictmod/help#file-formats">
            Formatting data FAQs<br>
          </router-link>
          <router-link to="/predictmod/help#run-sample">
            Run a prediction<br>
          </router-link>
          <router-link to="/predictmod/help#interpreting-results">
            Interpreting a prediction result<br>
          </router-link>
          <router-link to="/predictmod/help#r-nr">
            "Responder" vs "Non-responder" outcomes<br>
          </router-link>
          <router-link to="/predictmod/help#visualization">
            Data visualization examples and interpretations<br>
          </router-link>
          <router-link to="/predictmod/help#new-prediction">
            Run another prediction<br>
          </router-link>
        </v-card-text>
        </v-card>
        <v-card class="text-left" variant="flat">
          <v-card-title>
            Coming soon: Upload a Model
          </v-card-title>
          <v-card-text>
          <router-link to="/predictmod/help#coming-soon">
            Uploading your machine-learning model<br>
          </router-link>
          <router-link to="/predictmod/help#coming-soon">
            Model review & verification process<br>
          </router-link>
          <router-link to="/predictmod/help#coming-soon">
            Model Upload FAQs<br>
          </router-link>
        </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <HelpContent />

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
import HelpContent from '@/components/HelpContent.vue';

import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import LicenseShow from './LicenseShow.vue';

export default {

  name: 'Home',
  data() {
			return {
				home: false,
        text: `
# YO {#anchor1}
## YOYO {#anchor2}
### YOYOYO {#anchor3}
`
			}
    },
  components: { HelpContent, DisclaimerShow, LicenseShow }
}
</script>
