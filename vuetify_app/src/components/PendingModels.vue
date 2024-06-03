
<template>
    <!-- TODO: Virtual scroll isn't working as expected, defaults to not showing the fields. -->
<!-- <v-virtual-scroll :height="200"> -->
    <v-card v-for="obj in data" variant="flat" class="text-left">
    <v-card-text>
        <h4>Name: {{ obj.fields.name }}</h4>
        Version: {{ obj.fields.version }}<br>
        Data Type: {{ obj.fields.data_type }}<br>
    </v-card-text>
    </v-card>
<!-- </v-virtual-scroll> -->
</template>


<script>
export default {
    name: "PendingModels",
    props: {
        data: Object,
    },
    mounted() {
    },
}

</script>