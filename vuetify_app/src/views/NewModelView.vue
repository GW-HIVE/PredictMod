<template>
  <v-app>
    <v-container fluid>
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
                <h1>PredictMod: Model Submission</h1>
              </v-card-title>
              </v-card>
          </div>
        </div>
      </v-img>
    </v-banner>
  </v-container>

<v-container>
<h1>New Model Submission</h1>
Here are some sample instructions about how to handle model submission. <br>
Here's a follow-up paragraph of the same. <br>
Maybe we'll have some markdown here? <br>
Check if users are logged in. Give the option of uploads. What is the correct workflow? <br>
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
  </v-app>
  
  </template>
  <script>
  import { useAppStore } from '@/store/app';  // For user info
  import DisclaimerShow from '@/views/DisclaimerShow.vue';
  import LicenseShow from '@/views/LicenseShow.vue';
  
  // import { marked } from "marked";
  // import * as XLSX from 'xlsx';

  const modelsURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api/model-details/': "/predictmod/api/model-details/";
  
  export default {
  
    name: 'NewModelInstructions',
    setup() {
    //   console.log("---> Model view, initializing")
      const appStore = useAppStore();
      return { appStore };
    },
    mounted() {
      // TODO: Markdown is here
      // this.getMarkDown();
    },
    props: {
        // name: String,
    },
    data() {
        return {
            modelsURL: modelsURL,
            showDetails: false,
            modelDetails: null,
            name: "New Models"
        }
      },
    methods: {
      // TODO: Markdown
      // async getMarkDown() {
      //   const localURL = `${this.modelsURL}?q=${this.name}`
      //   // console.log("Getting details for: ", localURL);
      //   const res = await fetch(localURL, {
      //       method: 'GET',
      //   });
      //   if (!res.status == 200) {
      //       console.log("Error on return")
      //   };
      //   const response = await res.json();
      //   // console.log("Received response:\n", JSON.stringify(response));
      //   this.modelDetails = marked.parse(response.details);
      //   this.showDetails = true;
      // },
    },
    components: { DisclaimerShow, LicenseShow },
  }
  </script>
  