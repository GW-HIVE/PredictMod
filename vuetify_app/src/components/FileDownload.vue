<!-- 
    Adopted liberally from:
    https://github.com/bezkoder/vuetify-file-upload
 -->
<template>
    <div class="text-center">
          <v-btn color="primary" small @click.prevent="download">
            Download example data file
            <!-- <v-icon right dark>mdi-cloud-upload</v-icon> -->
          </v-btn>
    </div>
  </template>
  
  <script>

  import DownloadService from '@/services/DownloadService';
  import { useQueryState } from '@/store/queryState';

  // TODO: Deprecated component, ready for removal?

  export default {
    name: "download-files",
    setup() {
      const queryState = useQueryState();
      return { queryState }
    },
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
      triggerPreview() {
        queryState.downloadPreview = true;
      },
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