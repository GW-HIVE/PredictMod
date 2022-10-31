<template>
  <v-container>
    <v-img      
      src="./assets/HiveIcon.jpg"
			alignment="centered"
			max-height="150"
			max-width="250">
    </v-img>

    <v-row>
      <v-col lg="6">
            <v-card-title class="title font-weight-bold">
              Welcome to PredictMod!
              
            </v-card-title>
            
            <v-card-text class="text-left">
              PredictMod is a functional WebApp built using VueJS and powered by machine learning to help inform physicians' decisions. 
              PredictMod takes metagenomic microbiome or electronic health record data as 
              input and outputs a prediction of whether the ketogenic diet would be successful in managing prediabetes.
            </v-card-text>
    </v-col>
    
</v-row>

    <v-row>
      <v-col md="3">
          <SimpleUploadEHR/>
    </v-col>
      <v-col md="3">

          <SimpleUploadMG MGoutput="unsuccessful"/>

    </v-col>
  </v-row>
  
  <v-row>
    <v-col md="6">
        <DisclaimerShow/>
    </v-col>
  </v-row>

    
</v-container>





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