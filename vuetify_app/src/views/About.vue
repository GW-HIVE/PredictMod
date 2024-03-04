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
              <h1>PredictMod</h1>
            </v-card-title>
            <v-card-text class="text-center">
            <h4>A Machine Learning-Based Application for Informed Clinical Decision Making</h4>
            </v-card-text>
            </v-card>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
      </div>
      </div>
    </v-img>
  </v-banner>

  <v-container>


    <v-row>
      <v-col>
        
        <v-card-title class="title text-left font-weight-bold">
          About PredictMod
        </v-card-title>
        <v-card-text class="text-left">
          Our goal is to provide clinicians with a powerful decision making tool that enhances clinical 
          understanding of patient-level data. The PredictMod platform utilizes machine learning 
          tools and complex datasets based on electronic health records, gut microbiome, and -omics 
          data to forecast patient outcomes, often in response to treatment for a particular condition. 
          While our primary condition of interest is Prediabetes, the tool is designed to be used for a 
          variety of conditions, interventions, and data types.
        </v-card-text >
        <v-card-title class="title text-left font-weight-bold">
          About HIVE Lab
        </v-card-title>
        <v-card-text class="text-left">
          The HIVE Lab group is involved in developing the High-performance Integrated Virtual Environment (HIVE) 
          which aims to integrate various high throughput data analysis tools for bioinformatics. In 
          addition to the HIVE platform, the lab is involved in developing bioinformatics tools and resources, 
          such as standards for bioinformatics communication, knowledgebases for glycoinformatics and 
          infectious diseases, cancer research, and microbiome analysis.
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
