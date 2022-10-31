<template>	

	
		<button class="button is-light" @click="show = !show">
			DISCLAIMER
		</button>

		<v-card-text class="text-left" v-if="show"
		>
			We make no warranties regarding the 
			accuracy of the predictions, and disclaim liability 
			for damages resulting from its use. This portal is for 
			educational and informational purposes only and should not 
			be used instead of professional medical advice, treatment, or intervention.
		</v-card-text>


</template>

<script>
export default {
	data() {
			return {
				show: false,
				
			}
		},
		methods: {

		},
}
</script>
