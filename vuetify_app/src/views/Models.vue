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
              <h1>PredictMod Models</h1>
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

  <v-container fluid>
    <h1>Released Models</h1>
    <v-row dense>
      <v-col
        v-for="model in this.appStore.releasedModels"
        :key="model.fields.name"
      >
      <!-- :cols="model.flex" -->

      <!-- <v-card :href="this.modelsURL+model.fields.link"> -->
      <!-- :href="this.modelsURL+model.fields.link" -->
        <v-card @click.submit="goToTarget(model.fields.link)">
        <v-card-title v-text="model.fields.name"></v-card-title>
        <v-card-text>Version: {{ model.fields.version }} </v-card-text>
      </v-card>
      </v-col>

    </v-row>
</v-container>
<!--
<v-container fluid>
    <h1>Upcoming Models</h1>
    <v-row dense>
      <v-col
        v-for="model in this.appStore.pendingModels"
        :key="model.fields.name"
      >
      //!-- :cols="model.flex" -//->

      <v-card :href="this.modelsURL+model.fields.name">
        <v-card-title v-text="model.fields.name"></v-card-title>
        <v-card-text>Version: {{ model.fields.version }} </v-card-text>
      </v-card>

      </v-col>

    </v-row>
</v-container>
-->
<v-container fluid>
    <h1>Contribute to the PredictMod Platform</h1>
    <v-card :href="newModelsURL">
      <v-card-text>Learn how to submit new models and contribute to the PredictMod platform!</v-card-text>
    </v-card>
</v-container>

<v-container fluid>
    <h1>See how our example AI/ML pipeline can work for you!</h1>
    <v-card :href="tutorialURL">
      <v-card-text>Not sure where to start with AI/ML? Get started with our example workflow pipeline.</v-card-text>
    </v-card>
</v-container>

<v-container>
    <!-- <v-btn @click.submit="logModels()">Click to log models to console</v-btn> -->

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
import { useAppStore } from '@/store/app';
import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import LicenseShow from './LicenseShow.vue';

const modelsURL = 'models/';
const newModelsURL = 'https://hivelab.biochemistry.gwu.edu/wiki/PredictMod_Model_Submission'
const tutorialURL = 'https://hivelab.biochemistry.gwu.edu/wiki/PredictMod_ML_Pipeline_Tutorial'

export default {

  name: 'Models',
  setup() {
    // console.log("---> Model view, initializing")
    const appStore = useAppStore();
    return { appStore };
  },
  mounted() {
    if (!this.appStore.releasedModels) {
      this.appStore.getModels();
    };
  },
  data() {
			return {
				modelsURL: modelsURL,
        newModelsURL: newModelsURL,
        tutorialURL: tutorialURL,
      }
    },
  methods: {
    logModels() {
      console.log("Released models: ", JSON.stringify(this.appStore.releasedModels));
    },
    goToTarget(linkText) {
      // console.log("Targeting:\nBase URL: %s\nModel URL: %s", this.modelsURL, linkText);
      this.$router.push(this.modelsURL+linkText);
    },
  },
  components: { DisclaimerShow, LicenseShow }
}
</script>
