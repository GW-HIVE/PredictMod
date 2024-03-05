<template>
<div>
  <h3>
    Sample Chart with Live Data
  </h3>
  <div id="LiveChartArea">

  </div>
</div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'LiveChartTest',
  mounted() {
    this.retrieveData();
  },
  data() {
    return {
      chartData: null,
    }
  },
  methods: {
    async retrieveData() {
      const res = await fetch('http://localhost:8000/predictmod/api/live-data/', {
        method: "GET",
      })
      if (!res.ok) {
        console.log("Error on getting data: %s", res.ok);
        return;
      }
      this.data = await res.json();
      console.log("Recovered data: %s", JSON.stringify(this.data));
      console.log("---> Attempting to create chart");
      this.createChart();
    },
  createChart() {
    if (!this.data) {
      console.log("Error on chart creation!");
      return;
    }
    const margin = {top: 30, right: 30, bottom: 70, left: 60},
          width = 800 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

    const svg = d3.select("#LiveChartArea")
                  .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                    .attr("transform",`translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
                .range([0, width])
                .domain(this.data.map(d => d.name ))
                .padding(0.2);

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10, 0)rotate(-45)")
        .style("text-anchor", "end")

    const maxY = Math.max(...this.data.map(d => d.value), 1);
    const minY = Math.min(...this.data.map(d => d.value), 0);

    const y = d3.scaleLinear()
      .domain([minY, maxY])
      .range([height, 0]);

    svg.append("g")
      .call(d3.axisLeft(y));
    console.log("...Y Axis created");

    // Bars
    svg.selectAll("mybars")
      .data(this.data)
      .enter()
      .append("rect")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.value))
    },

  },
}

</script>