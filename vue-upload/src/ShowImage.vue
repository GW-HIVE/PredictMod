<template>	

	<v-container>
		
		<button class="button is-primary is-boxed" @click="awesome = !awesome">
			Toggle Image
		</button>
		
			<v-img v-if="awesome"
				justify="center"
				alignment="center"
				src="./assets/logo.png"
				max-height="150"
				max-width="250"
			></v-img>
</v-container>

</template>



<script>
export default {
data() {
		return {
			awesome: false
		}
	}
}
</script>