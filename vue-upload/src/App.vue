<template>
  <div class="section">
    <div class="container">

    </div>
  </div>



    <div class="container">
      <div class="title is-centered">
        Welcome to PredictMod!
      </div> 
      </div>
  
    <div class="container">

      <simple-upload />
      <simple-upload-e-h-r />
    </div>
  

</template>
<script>
import SimpleUpload from './SimpleUpload.vue';
import SimpleUploadEHR from './SimpleUploadEHR.vue';

export default {
  name: 'App',
  components: { SimpleUpload, SimpleUploadEHR }
}
</script>