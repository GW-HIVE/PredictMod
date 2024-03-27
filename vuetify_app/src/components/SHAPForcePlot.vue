<template>
    <h3>
        Live SHAP Data
    </h3>
    <div class="container">
      <v-row>
        <svg width="600" height="400"></svg>
      </v-row>
    </div>
    <v-btn @click="rerender()">
      Rerender
    </v-btn>
</template>

<script>
import { select } from "d3-selection";
import { scaleLinear } from "d3-scale";
import { format } from "d3-format";
import { axisBottom } from "d3-axis";
import { line } from "d3-shape";
import { hsl } from "d3-color";

import {
  sortBy,
  map,
  each,
  sum,
  filter,
  findIndex,
  debounce
} from "lodash";
import colorsSet from "./color-set";

export default {
  name: "SHAPForcePlot",
  mounted() {
    this.createChart();
  },
  data() {
    return {
      plot_color: "RGBDDDD",
    }
  },
  props: {
    chartData: Object,
    plot_cmap: {
      type: String,
      default: "RdBu",
    }
  },
  methods: {
    rerender() {
      console.log("---> Calling draw <---");
      this.createChart();
    },
    createChart() {
  
      const svg = select("svg")

      // Adapted liberally from the SHAP repository under the MIT license
      // create our permanent elements
      const mainGroup = svg.append("g");
      const axisElement = mainGroup
        .append("g")
        .attr("transform", "translate(0,35)")
        .attr("class", "force-bar-axis");
      const onTopGroup = svg.append("g");
      const baseValueTitle = svg.append("text");
      const joinPointLine = svg.append("line");
      const joinPointLabelOutline = svg.append("text");
      const joinPointLabel = svg.append("text");
      const joinPointTitleLeft = svg.append("text");
      const joinPointTitleLeftArrow = svg.append("text");
      const joinPointTitle = svg.append("text");
      const joinPointTitleRightArrow = svg.append("text");
      const joinPointTitleRight = svg.append("text");

  // Define the tooltip objects
  const hoverLabelBacking = svg.append("text")
    .attr("x", 10)
    .attr("y", 20)
    .attr("text-anchor", "middle")
    .attr("font-size", 12)
    .attr("stroke", "#fff")
    .attr("fill", "#fff")
    .attr("stroke-width", "4")
    .attr("stroke-linejoin", "round")
    .text("")
    .on("mouseover", () => {
      hoverLabel.attr("opacity", 1);
      hoverLabelBacking.attr("opacity", 1);
    })
    .on("mouseout", () => {
      hoverLabel.attr("opacity", 0);
      hoverLabelBacking.attr("opacity", 0);
    });
  const hoverLabel = svg.append("text")
    .attr("x", 10)
    .attr("y", 20)
    .attr("text-anchor", "middle")
    .attr("font-size", 12)
    .attr("fill", "#0f0")
    .text("")
    .on("mouseover", () => {
      hoverLabel.attr("opacity", 1);
      hoverLabelBacking.attr("opacity", 1);
    })
    .on("mouseout", () => {
      hoverLabel.attr("opacity", 0);
      hoverLabelBacking.attr("opacity", 0);
    });

  // Create our colors and color gradients
  // Verify custom color map
  let plot_colors=undefined;
  if (typeof this.plot_cmap === "string")
  {
    if (!(this.plot_cmap in colorsSet.colors))
    {
      console.log("Invalid color map name, reverting to default.");
      plot_colors=colorsSet.colors.RdBu;
    }
    else
    {
      plot_colors = colorsSet.colors[this.plot_cmap]
    }
  }
  else if (Array.isArray(this.plot_cmap)){
    plot_colors = this.plot_cmap
  }
  const colors = plot_colors.map(x => hsl(x));
  const brighterColors = [1.45, 1.6].map((v, i) => colors[i].brighter(v));
  colors.map((c, i) => {
    const grad = svg
      .append("linearGradient")
      .attr("id", "linear-grad-" + i)
      .attr("x1", "0%")
      .attr("y1", "0%")
      .attr("x2", "0%")
      .attr("y2", "100%");
    grad
      .append("stop")
      .attr("offset", "0%")
      .attr("stop-color", c)
      .attr("stop-opacity", 0.6);
    grad
      .append("stop")
      .attr("offset", "100%")
      .attr("stop-color", c)
      .attr("stop-opacity", 0);
    const grad2 = svg
      .append("linearGradient")
      .attr("id", "linear-backgrad-" + i)
      .attr("x1", "0%")
      .attr("y1", "0%")
      .attr("x2", "0%")
      .attr("y2", "100%");
    grad2
      .append("stop")
      .attr("offset", "0%")
      .attr("stop-color", c)
      .attr("stop-opacity", 0.5);
    grad2
      .append("stop")
      .attr("offset", "100%")
      .attr("stop-color", c)
      .attr("stop-opacity", 0);
  });

    // create our x axis
    const tickFormat = format(",.4");
    const scaleCentered = scaleLinear();
    const axis = axisBottom()
      .scale(scaleCentered)
      .tickSizeInner(4)
      .tickSizeOuter(0)
      .tickFormat(d => tickFormat(invLinkFunction(d)))
      .tickPadding(-18);

    // draw and then listen for resize events
    //this.draw();
    window.addEventListener("resize", this.redraw);
    window.setTimeout(this.redraw, 50); // re-draw after interface has updated

    // copy the feature names onto the features
    each(this.chartData.featureNames, (n, i) => {
      if (this.chartData.features[i]) {
        console.log("%s: %s", n, JSON.stringify(this.chartData.features[i]));
        this.chartData.features[i].name = n;
      }
    });

    // create our link function
    let invLinkFunction = undefined;
    if (this.chartData.link === "identity") {
      invLinkFunction = x => this.chartData.baseValue + x;
    } else if (this.chartData.link === "logit") {
      invLinkFunction = x =>
        1 / (1 + Math.exp(-(this.chartData.baseValue + x))); // logistic is inverse of logit
    } else {
      console.log("ERROR: Unrecognized link function: ", this.chartData.link);
    }

    // Set the dimensions of the plot
    // let width = svg?.node().parentNode.offsetWidth;
    let width = svg.node() ? svg.node().parentNode.offsetWidth : 0;
    // if (width == 0) return setTimeout(() => this.draw(this.chartData), 500);
    svg.style("height", 150 + "px");
    svg.style("width", width + "px");
    let topOffset = 50;

    let data = sortBy(this.chartData.features, x => -1 / (x.effect + 1e-10));
    let totalEffect = sum(map(data, x => Math.abs(x.effect)));
    let totalPosEffects =
      sum(map(filter(data, x => x.effect > 0), x => x.effect)) || 0;
    let totalNegEffects =
      sum(map(filter(data, x => x.effect < 0), x => -x.effect)) || 0;
    const domainSize = Math.max(totalPosEffects, totalNegEffects) * 3;
    let scale = scaleLinear()
      .domain([0, domainSize])
      .range([0, width]);
    let scaleOffset = width / 2 - scale(totalNegEffects);

    scaleCentered
      .domain([-domainSize / 2, domainSize / 2])
      .range([0, width])
      .clamp(true);
    axisElement
      .attr("transform", "translate(0," + topOffset + ")")
      .call(axis);

    // calculate the position of the join point between positive and negative effects
    // and also the positions of each feature effect block
    let pos = 0,
      i,
      joinPoint,
      joinPointIndex;
    for (i = 0; i < data.length; ++i) {
      data[i].x = pos;
      if (data[i].effect < 0 && joinPoint === undefined) {
        joinPoint = pos;
        joinPointIndex = i;
      }
      pos += Math.abs(data[i].effect);
    }
    if (joinPoint === undefined) {
      joinPoint = pos;
      joinPointIndex = i;
    }

    let lineFunction = line()
      .x(d => d[0])
      .y(d => d[1]);

    let getLabel = d => {
      if (d.value !== undefined && d.value !== null && d.value !== "") {
        return (
          d.name +
          " = " +
          (isNaN(d.value) ? d.value : tickFormat(d.value))
        );
      } else return d.name;
    };

    data = this.chartData.hideBars ? [] : data;
    let blocks = mainGroup.selectAll(".force-bar-blocks").data(data);
    blocks
      .enter()
      .append("path")
      .attr("class", "force-bar-blocks")
      .merge(blocks)
      .attr("d", (d, i) => {
        let x = scale(d.x) + scaleOffset;
        let w = scale(Math.abs(d.effect));
        let pointShiftStart = d.effect < 0 ? -4 : 4;
        let pointShiftEnd = pointShiftStart;
        if (i === joinPointIndex) pointShiftStart = 0;
        if (i === joinPointIndex - 1) pointShiftEnd = 0;
        return lineFunction([
          [x, 6 + topOffset],
          [x + w, 6 + topOffset],
          [x + w + pointShiftEnd, 14.5 + topOffset],
          [x + w, 23 + topOffset],
          [x, 23 + topOffset],
          [x + pointShiftStart, 14.5 + topOffset]
        ]);
      })
      .attr("fill", d => (d.effect > 0 ? colors[0] : colors[1]))
      .on("mouseover", d => {
        if (scale(Math.abs(d.effect)) < scale(totalEffect) / 50 ||
            scale(Math.abs(d.effect)) < 10) {
          let x = scale(d.x) + scaleOffset;
          let w = scale(Math.abs(d.effect));
          hoverLabel
            .attr("opacity", 1)
            .attr("x", x + w/2)
            .attr("y", topOffset + 0.5)
            .attr("fill", d.effect > 0 ? colors[0] : colors[1])
            .text(getLabel(d));
          hoverLabelBacking
            .attr("opacity", 1)
            .attr("x", x + w/2)
            .attr("y", topOffset + 0.5)
            .text(getLabel(d));
        }
      })
      .on("mouseout", () => {
        hoverLabel.attr("opacity", 0);
        hoverLabelBacking.attr("opacity", 0);
      });
    blocks.exit().remove();

    let filteredData = filter(data, d => {
      return (
        scale(Math.abs(d.effect)) > scale(totalEffect) / 50 &&
        scale(Math.abs(d.effect)) > 10
      );
    });

    let labels = onTopGroup
      .selectAll(".force-bar-labels")
      .data(filteredData);
    labels.exit().remove();
    labels = labels
      .enter()
      .append("text")
      .attr("class", "force-bar-labels")
      .attr("font-size", "12px")
      .attr("y", 48 + topOffset)
      .merge(labels)
      .text(d => {
        if (d.value !== undefined && d.value !== null && d.value !== "") {
          return (
            d.name +
            " = " +
            (isNaN(d.value) ? d.value : tickFormat(d.value))
          );
        } else return d.name;
      })
      .attr("fill", d => (d.effect > 0 ? colors[0] : colors[1]))
      .attr("stroke", function(d) {
        d.textWidth = Math.max(
          this.getComputedTextLength(),
          scale(Math.abs(d.effect)) - 10
        );
        d.innerTextWidth = this.getComputedTextLength();
        return "none";
      });
    this.filteredData = filteredData;

    // compute where the text labels should go
    if (data.length > 0) {
      pos = joinPoint + scale.invert(5);
      for (let i = joinPointIndex; i < data.length; ++i) {
        data[i].textx = pos;
        pos += scale.invert(data[i].textWidth + 10);
      }
      pos = joinPoint - scale.invert(5);
      for (let i = joinPointIndex - 1; i >= 0; --i) {
        data[i].textx = pos;
        pos -= scale.invert(data[i].textWidth + 10);
      }
    }

    labels
      .attr(
        "x",
        d =>
          scale(d.textx) +
          scaleOffset +
          (d.effect > 0 ? -d.textWidth / 2 : d.textWidth / 2)
      )
      .attr("text-anchor", "middle"); //d => d.effect > 0 ? 'end' : 'start');

    // Now that we know the text widths we further filter by what fits on the screen
    filteredData = filter(filteredData, d => {
      return (
        scale(d.textx) + scaleOffset > this.chartData.labelMargin &&
        scale(d.textx) + scaleOffset < width - this.chartData.labelMargin
      );
    });
    this.filteredData2 = filteredData;

    // Build an array with one extra feature added
    let filteredDataPlusOne = filteredData.slice();
    let ind = findIndex(data, filteredData[0]) - 1;
    if (ind >= 0) filteredDataPlusOne.unshift(data[ind]);

    let labelBacking = mainGroup
      .selectAll(".force-bar-labelBacking")
      .data(filteredData);
    labelBacking
      .enter()
      .append("path")
      .attr("class", "force-bar-labelBacking")
      .attr("stroke", "none")
      .attr("opacity", 0.2)
      .merge(labelBacking)
      .attr("d", d => {
        return lineFunction([
          [
            scale(d.x) + scale(Math.abs(d.effect)) + scaleOffset,
            23 + topOffset
          ],
          [
            (d.effect > 0 ? scale(d.textx) : scale(d.textx) + d.textWidth) +
              scaleOffset +
              5,
            33 + topOffset
          ],
          [
            (d.effect > 0 ? scale(d.textx) : scale(d.textx) + d.textWidth) +
              scaleOffset +
              5,
            54 + topOffset
          ],
          [
            (d.effect > 0 ? scale(d.textx) - d.textWidth : scale(d.textx)) +
              scaleOffset -
              5,
            54 + topOffset
          ],
          [
            (d.effect > 0 ? scale(d.textx) - d.textWidth : scale(d.textx)) +
              scaleOffset -
              5,
            33 + topOffset
          ],
          [scale(d.x) + scaleOffset, 23 + topOffset]
        ]);
      })
      .attr("fill", d => `url(#linear-backgrad-${d.effect > 0 ? 0 : 1})`);
    labelBacking.exit().remove();

    let labelDividers = mainGroup
      .selectAll(".force-bar-labelDividers")
      .data(filteredData.slice(0, -1));
    labelDividers
      .enter()
      .append("rect")
      .attr("class", "force-bar-labelDividers")
      .attr("height", "21px")
      .attr("width", "1px")
      .attr("y", 33 + topOffset)
      .merge(labelDividers)
      .attr(
        "x",
        d =>
          (d.effect > 0 ? scale(d.textx) : scale(d.textx) + d.textWidth) +
          scaleOffset +
          4.5
      )
      .attr("fill", d => `url(#linear-grad-${d.effect > 0 ? 0 : 1})`);
    labelDividers.exit().remove();

    let labelLinks = mainGroup
      .selectAll(".force-bar-labelLinks")
      .data(filteredData.slice(0, -1));
    labelLinks
      .enter()
      .append("line")
      .attr("class", "force-bar-labelLinks")
      .attr("y1", 23 + topOffset)
      .attr("y2", 33 + topOffset)
      .attr("stroke-opacity", 0.5)
      .attr("stroke-width", 1)
      .merge(labelLinks)
      .attr("x1", d => scale(d.x) + scale(Math.abs(d.effect)) + scaleOffset)
      .attr(
        "x2",
        d =>
          (d.effect > 0 ? scale(d.textx) : scale(d.textx) + d.textWidth) +
          scaleOffset +
          5
      )
      .attr("stroke", d => (d.effect > 0 ? colors[0] : colors[1]));
    labelLinks.exit().remove();

    let blockDividers = mainGroup
      .selectAll(".force-bar-blockDividers")
      .data(data.slice(0, -1));
    blockDividers
      .enter()
      .append("path")
      .attr("class", "force-bar-blockDividers")
      .attr("stroke-width", 2)
      .attr("fill", "none")
      .merge(blockDividers)
      .attr("d", d => {
        let pos = scale(d.x) + scale(Math.abs(d.effect)) + scaleOffset;
        return lineFunction([
          [pos, 6 + topOffset],
          [pos + (d.effect < 0 ? -4 : 4), 14.5 + topOffset],
          [pos, 23 + topOffset]
        ]);
      })
      .attr("stroke", (d, i) => {
        if (joinPointIndex === i + 1 || Math.abs(d.effect) < 1e-8)
          return "#rgba(0,0,0,0)";
        else if (d.effect > 0) return brighterColors[0];
        else return brighterColors[1];
      });
    blockDividers.exit().remove();

    joinPointLine
      .attr("x1", scale(joinPoint) + scaleOffset)
      .attr("x2", scale(joinPoint) + scaleOffset)
      .attr("y1", 0 + topOffset)
      .attr("y2", 6 + topOffset)
      .attr("stroke", "#F2F2F2")
      .attr("stroke-width", 1)
      .attr("opacity", 1);

    joinPointLabelOutline
      .attr("x", scale(joinPoint) + scaleOffset)
      .attr("y", -5 + topOffset)
      .attr("color", "#fff")
      .attr("text-anchor", "middle")
      .attr("font-weight", "bold")
      .attr("stroke", "#fff")
      .attr("stroke-width", 6)
      .text(format(",.2f")(invLinkFunction(joinPoint - totalNegEffects)))
      .attr("opacity", 1);
    console.log(
      "joinPoint",
      joinPoint,
      scaleOffset,
      topOffset,
      totalNegEffects
    );
    joinPointLabel
      .attr("x", scale(joinPoint) + scaleOffset)
      .attr("y", -5 + topOffset)
      .attr("text-anchor", "middle")
      .attr("font-weight", "bold")
      .attr("fill", "#000")
      .text(format(",.2f")(invLinkFunction(joinPoint - totalNegEffects)))
      .attr("opacity", 1);

    joinPointTitle
      .attr("x", scale(joinPoint) + scaleOffset)
      .attr("y", -22 + topOffset)
      .attr("text-anchor", "middle")
      .attr("font-size", "12")
      .attr("fill", "#000")
      .text(this.chartData.outNames[0])
      .attr("opacity", 0.5);

    if (!this.chartData.hideBars) {
      joinPointTitleLeft
        .attr("x", scale(joinPoint) + scaleOffset - 16)
        .attr("y", -38 + topOffset)
        .attr("text-anchor", "end")
        .attr("font-size", "13")
        .attr("fill", colors[0])
        .text("higher")
        .attr("opacity", 1.0);
      joinPointTitleRight
        .attr("x", scale(joinPoint) + scaleOffset + 16)
        .attr("y", -38 + topOffset)
        .attr("text-anchor", "start")
        .attr("font-size", "13")
        .attr("fill", colors[1])
        .text("lower")
        .attr("opacity", 1.0);

      joinPointTitleLeftArrow
        .attr("x", scale(joinPoint) + scaleOffset + 7)
        .attr("y", -42 + topOffset)
        .attr("text-anchor", "end")
        .attr("font-size", "13")
        .attr("fill", colors[0])
        .text("→")
        .attr("opacity", 1.0);
      joinPointTitleRightArrow
        .attr("x", scale(joinPoint) + scaleOffset - 7)
        .attr("y", -36 + topOffset)
        .attr("text-anchor", "start")
        .attr("font-size", "13")
        .attr("fill", colors[1])
        .text("←")
        .attr("opacity", 1.0);
    }
    if (!this.chartData.hideBaseValueLabel) {
      baseValueTitle
        .attr("x", scaleCentered(0))
        .attr("y", -22 + topOffset)
        .attr("text-anchor", "middle")
        .attr("font-size", "12")
        .attr("fill", "#000")
        .text("base value")
        .attr("opacity", 0.5);
    }
    console.log("Made it here ....")
    }
  },
  computed: {
  },
}
</script>

