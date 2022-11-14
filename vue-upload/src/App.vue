<template>
  <v-banner lg="6">
    <v-img
      src="./assets/Banner.png">
    </v-img>
  </v-banner>

  <v-container>

    <v-row>
      <v-col>
            <v-card-title class="title text-left font-weight-bold">
              Welcome to PredictMod!
              
            </v-card-title>
            <v-card-text class="text-left">
              PredictMod is a functional web app built using VueJS and powered by machine learning to help inform physicians' decisions. 
              PredictMod takes metagenomic microbiome or electronic health record (EHR) data as 
              input and outputs a prediction of whether the ketogenic diet would be successful in managing prediabetes. 

            </v-card-text>


      </v-col>
    
    </v-row>
    <v-row>
      <v-col>
        <v-card-text class = "text-left">
          For more information, click the links below to explore the GitHub and SharePoint pages:
        </v-card-text>
        <v-breadcrumbs>
          <v-breadcrumbs-item href="https://github.com/GW-HIVE/PredictMod"> PredictMod Repo </v-breadcrumbs-item>
          <v-breadcrumbs-item href="https://gwu0.sharepoint.com/sites/PredictMod-GRP"> SharePoint Page </v-breadcrumbs-item>
        </v-breadcrumbs>  
      </v-col>

    </v-row>




  <v-card>
    <v-row>
          <v-col>
            <SimpleUploadEHR/>
          </v-col>
          <v-col>
            <SimpleUploadMG/>
          </v-col>

    </v-row>
  

    <v-row>
      <v-col>
          <DisclaimerShow/>
      </v-col>
    </v-row>
  </v-card>

</v-container>

<v-footer dark padless>
  <v-img
      src="./assets/Footer.png"
      alignment="centered">
  </v-img>
</v-footer>


</template>
<script>
import SimpleUploadMG from './SimpleUploadMG.vue';
import SimpleUploadEHR from './SimpleUploadEHR.vue';
import DisclaimerShow from './DisclaimerShow.vue';


export default {
  name: 'App',
  components: { SimpleUploadMG, SimpleUploadEHR, DisclaimerShow}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>