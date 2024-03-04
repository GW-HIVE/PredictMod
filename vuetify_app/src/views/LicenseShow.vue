<template>	

	
		<!-- <button class="button is-light" @click="show = true">
			LICENSE
		</button> -->

		<v-card-title>
			<h3>LICENSE</h3>
		</v-card-title>

		<v-card-text class="text-center" v-if="show"
		>
		We have chosen to apply the Creative Commons Attribution 4.0 International (CC BY 4.0) 
		license to all our database sets. This means that you are free to copy, distribute, 
		display and make commercial use of these databases in all legislations, provided you give us credit.
		</v-card-text>


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
