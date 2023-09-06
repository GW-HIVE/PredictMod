<template>

  <v-col>
    <router-link to="/upload-mg">
  	<v-img
  		src="../assets/MG_Model.jpg"
  		contain
  	/>
    </router-link>
  	<v-card-text>
  		The gut microbiome consists of the genetic material of microbial communities found within the human gastrointestinal tract.
  	</v-card-text>
  </v-col>
	
</template>

<script>
import SimpleUploadMG from './SimpleUploadMG.vue';

export default {
	data() {
			return {
				show: true,
			}
		},
		methods: {
		},
		components: { SimpleUploadMG }
}
</script>
