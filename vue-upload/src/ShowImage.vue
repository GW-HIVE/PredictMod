<template>	

	<v-container>
		
		<button class="button is-primary is-boxed" @click="show = !show">
			Show Results
		</button>

		<v-img class="mx-auto" v-if="show"
			src="./assets/logo.png"
			alignment="centered"
			max-height="150"
			max-width="250"
		>
		</v-img>

</v-container>

</template>



<script>
import axios from 'axios';
export default {
data() {
		return {
			show: false,
			
		}
	},
	methods: {

//tries to get image from /uploads-EHR folder
async function() {
	this.image = './uploads-EHR/w10003.png'
	axios.get(this.image,  )
	this.show = true
}

},

}
</script>