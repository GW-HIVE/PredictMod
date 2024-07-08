<template>
    <v-card v-for="obj in data" variant="flat" class="text-left">
    <v-card-title>
        <a :href=modelsURL+obj.fields.link>{{ obj.fields.name }}</a>
    </v-card-title>
    <v-card-text>
        Version: {{ obj.fields.version }}<br>
        Release Date: {{ obj.fields.release_date }}<br>
        Data Type: {{ obj.fields.data_type }}<br>
        Model Properties:<br>
        <span v-for="(value, key) in obj.fields.data_meta">
            &nbsp;-&nbsp;<b>{{ key }}</b>: {{ value }}<br>
        </span>
        Model Type: {{ obj.fields.model_type }}
    </v-card-text>
    </v-card>
</template>

<script>

const modelsURL = '/predictmod/models/'
// const modelsURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/models/': "/predictmod/models/";

export default {
    name: "ReleasedModels",
    props: {
        data: Object,
    },
    data() {
        return {
            modelsURL: modelsURL,
        }
    },
    mounted() {
    },
}

</script>
