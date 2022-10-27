<template>
  
  <div class="main">
    <div class="container">
    </div>
  </div>

    <div class="container">
      <div class="title">
        Welcome to PredictMod!
      </div> 
      </div>
  
    <div class="container">

      <simple-upload-m-g />

    <div class="container">

    </div>

      <simple-upload-e-h-r />

    <div class="container">

      <ShowImage />
     </div>

    </div>




</template>
<script>
import SimpleUploadMG from './SimpleUploadMG.vue';
import SimpleUploadEHR from './SimpleUploadEHR.vue';
import ShowImage from './ShowImage.vue'

export default {
  name: 'App',
  components: { SimpleUploadMG, SimpleUploadEHR, ShowImage }
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