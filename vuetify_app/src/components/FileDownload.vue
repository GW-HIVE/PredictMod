<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
    <div class="text-center">
      <!-- <v-row no-gutters justify="center" align="center"> -->
        <!-- <v-col cols="8"> -->
        <!-- <v-col> -->
            <!-- 
                See `rules` for filtering on file type. 
                Not super critical at present. 
             -->
          <!-- <v-file-input
            show-size
            label="Select a PredictMod-formatted xls or xlsx file"
            type="File"
            v-model="currentFile"
          ></v-file-input> -->
        <!-- </v-col> -->
        <!--
            This appears to break when invoked using Vuetify auto-magic 
            @change="selectFile($event)" 
        -->
            
        <!-- <v-col cols="4" class="pl-2"> -->
        <!-- <v-container class="justify-center"> -->
        <!-- <v-row> -->
        <!-- <v-col class="justify-center">   -->
          <v-btn color="primary" small @click.prevent="download">
            Download example data file
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
          </v-btn>
        <!-- </v-col> -->
        <!-- <v-col>
          <v-btn right color="success" dark small @click="upload">
            Submit & Analyze
          </v-btn>
        </v-col> -->
      <!-- </v-row> -->
    <!-- </v-container> -->
      <!-- </v-row> -->
  
      <!-- <v-alert v-if="message" color="blue-grey" dark>
        {{ message }}
      </v-alert> -->
      <!-- <v-row>
        <BarChart v-if="showChart" /> 
      </v-row> -->
    </div>
  </template>
  
  <script>

  import DownloadService from '@/services/DownloadService';

  export default {
    name: "download-files",
    props: {
        downloadTargetURL: String,
    },
    // components: { BarChart },
    // data() {
    //   return {
    //     currentFile: null,
    //     data: null,
    //     progress: 0,
    //     message: "Data must be selected before results are available",
    //     showChart: false,
    //   };
    // },
    methods: {
      download() {
        const response = DownloadService.download(this.downloadTargetURL, () => {
        })
        // console.log('---> FileDownload, got\n%s', JSON.stringify(response));
          // .then((response) => {
          //   // this.message = response.data.message;
          //   console.log('---> FileDownload, got\n%s', JSON.stringify(response));
          //   return response;
          // })
          // .catch(() => {
          //   this.progress = 0;
          //   this.message = "Could not download the file!";
          //   // this.currentFile = null;
          //   // this.data = null;
          // });
      },
    },
  };

  </script>