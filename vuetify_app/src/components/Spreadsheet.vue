<template>
<div ref="htmlout" />
</template>

<script>
import canvasDatagrid from 'canvas-datagrid';

export default {
    name: "Spreadsheet",
    data() {
        return {
            xlsData: null,
        }
    },
    props: {
        sheetData: Object,
    },
    mounted() {
        this.setUpSpreadsheet();
    },

    methods: {
        setUpSpreadsheet() {
            // Get element
            const element = this.$refs.htmlout;
            element.style.height = 250 + "px";
            element.style.width = 800 + "px";
            // console.log("Setting up spreadsheet canvas! Element is", element);
            // console.log("Data: \n", this.sheetData);
            const cdg = canvasDatagrid({
                parentNode: element,
                // autoResizeColumns: true,
            })
            // NB - Arbitrary collapse of cell width on canvas 
            //      may still lead to "canvas max" errors. 
            //      See SO: https://stackoverflow.com/a/53677532 for possible solution

            cdg.style.cellWidth = 50;
            cdg.data = this.sheetData

            cdg.style.height = '100%';
            cdg.style.width = '100%';
        },
    }
}

</script>