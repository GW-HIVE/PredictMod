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
              <v-card-title class="title text-center font-weight-bold center">
              <h1>Frequently Asked Questions</h1>
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
        <!-- <v-card variant="flat"> -->
        <v-card-title class="title text-left font-weight-bold">
          How can I run a prediction using my single-patient data file?
        </v-card-title>
        <v-card-text class="text-left">
          Use the query builder to select the desired condition, intervention, and data type 
          associated with your patient data. File upload templates vary by model. Reference 
          our example files to ensure your data meets our formatting requirements. 
          Select ‘Run Analysis’ to view the results. 

          <br><br>For additional assistance with uploading and formatting data, please contact our team.

        </v-card-text >
        <!-- </v-card> -->
        <!-- <v-card variant="flat"> -->
          <v-card-title class="title text-left font-weight-bold">
            Will the system store patient data?
          </v-card-title>
          <v-card-text class="text-left">
            The data will not be saved in the system. PredictMod will use uploaded patient data to make a one-time prediction.
          </v-card-text>
          <!-- </v-card> -->
        <!-- <v-card variant="flat"> -->
          <v-card-title class="title text-left font-weight-bold">
            What are the possible prediction outcomes?
          </v-card-title>
          <v-card-text class="text-left">
            PredictMod will provide a prediction categorized as either Responder or Non-Responder. 
            The outcomes associated with the response status vary for each model, 
            though a Responder result is generally associated with a positive health outcome, 
            and the Non-Responder result is generally associated with a negative health outcome. 

            <br><br>For additional information, please review the model information below.
          </v-card-text>
          <!-- </v-card> -->
      <!-- <v-card variant="flat"> -->
        <v-card-title class="title text-left font-weight-bold">
          What data types are included in the PredictMod query selection?
        </v-card-title>
        <v-card-text class="text-left">
          The current data types are metagenomic (MG) and electronic health record (EHR). We also have a glycomics data type coming soon.

          <br><br>MG data consist of the microbial composition of the gut microbiome typically displayed as a percent of abundance. 
          This data is typically used within a research context to profile healthy gut microbiomes and to identify 
          differential abundances and their associations to disease. Our MG Model is trained on publicly available data. 
          The reference genomes used for this model are recorded in the <a href="https://hive.biochemistry.gwu.edu/gfkb" >Gut Feeling Knowledge Base (GFKB).</a> 
          Please use this list as a reference. Organisms not referenced in the GFKB can still be included in the input
           and receive an accurate model prediction. If you have any questions about this, please don’t hesitate to contact our team. 

           <br><br>EHR consists of real-time patient-centered records that are utilized by physicians to streamline their workflow. 
          It provides physicians the ability to view important medical details about their patients in order to 
          provide improved patient care that is both efficient and safe. Our EHR models are trained on data from the MDClone and Epic Cosmos.
        </v-card-text>
      <!-- </v-card> -->
      <!-- <v-card variant="flat"> -->
        <v-card-title class="title text-left font-weight-bold">
          What conditions are included in the PredictMod query selection?
        </v-card-title>
        <v-card-text class="text-left">
          The current condition of interest is Prediabetes. We also have an Epilepsy model coming soon.

          <br><br>Prediabetes is a precursor to Type 2 Diabetes Mellitus (T2DM), where blood sugars are higher than normal, 
          but not high enough to be considered T2DM. Prediction outcomes are based on a 5% reduction 
          in weight, HOMA-IR, or a diagnosis of T2DM.
        </v-card-text>
      <!-- </v-card> -->
      <!-- <v-card variant="flat"> -->
        <v-card-title class="title text-left font-weight-bold">
          What interventions are included in the PredictMod query selection?
        </v-card-title>
        <v-card-text class="text-left">
          The current interventions are exercise, ketogenic diet, and dietary counseling. 
          
          <br><br>We also have a Semaglutide intervention coming soon.
        </v-card-text>
      <!-- </v-card> -->
      <!-- <v-card>
        <v-card-title class="title text-left font-weight-bold">

        </v-card-title>
        <v-card-text class="text-left">

        </v-card-text>
      </v-card> -->
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
