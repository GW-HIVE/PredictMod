<template>	

	<v-col>
	  <router-link to="/predictmod/ehr-home">
		<v-img
			src="../assets/EHR_Model.jpg"
			:aspect-ratio="16 / 9"
			contain
		/>
	  </router-link>
		<v-card-text>
			Electronic Health Records (EHR) contain patient-centered clinical records obtained through regular medical checkups.
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
