<template>	

	
		<!-- <button class="button is-light" @click="show = true">
			DISCLAIMER
		</button> -->
		<v-card variant="tonal">
		<v-card-title>
			<h3>DISCLAIMER</h3>
		</v-card-title>
		<v-card-text class="text-center" v-if="show"
		>
		We make no guarantees on the accuracy of the predictions, and disclaim liability from 
		damages resulting from its use. This site is for educational and informational 
		purposes only, and should not be used instead of medical advice, treatment, or intervention.

		</v-card-text>
	</v-card>

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
