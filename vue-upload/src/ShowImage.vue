<template>	

	<v-container>
		
		<button class="button is-primary is-boxed" @click="getImage">
			Toggle Image
		</button>
		
			<v-img v-if="show"
				justify="center"
				alignment="center"
				src="image"
				max-height="150"
				max-width="250"
			></v-img>
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
async getImage() {
	this.image = './uploads-EHR/w10003.png'
	axios.get(this.image,  )
	this.show = true
}

},

}
</script>