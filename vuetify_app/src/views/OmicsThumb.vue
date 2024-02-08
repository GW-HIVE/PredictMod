<template>	

	<v-col>
	  <router-link to="/predictmod/omics-home">
		<v-img
			src="../assets/Omics_Model.jpg"
			:aspect-ratio="16 / 9"
			contain
		/>
	  </router-link>
		<v-card-text>
			'Omics models built up from various data sources, e.g. Glycomics and Metagenomics.
		</v-card-text>
	</v-col>
	
</template>

<script>
export default {
	data() {
			return {
				show: true,
				
			}
		},
		methods: {

		},
}
</script>
