var width = 960,
    height = 500,
    nodeSize = 30;

var color = d3.scale.category20();

var svg = d3.select("#detail-claim").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("{{ url_for('static', filename='data/data-neuron.json') }}", function(error, graph) {
    var nodes = graph.nodes;

    // get network size
    var netsize = {};
    nodes.forEach(function (d) {
      if(d.layer in netsize) {
          netsize[d.layer] += 1;
      } else {
          netsize[d.layer] = 1;
      }
      d["lidx"] = netsize[d.layer];
    });

    // calc distances between nodes
    var largestLayerSize = Math.max.apply(
        null, Object.keys(netsize).map(function (i) { return netsize[i]; }));

    var xdist = width / Object.keys(netsize).length,
        ydist = height / largestLayerSize;

    // create node locations
    nodes.map(function(d) {
      d["x"] = (d.layer - 0.5) * xdist;
      d["y"] = (d.lidx - 0.5) * ydist;
    });

    // autogenerate links
    var links = [];
    nodes.map(function(d, i) {
      for (var n in nodes) {
        if (d.layer + 1 == nodes[n].layer) {
          links.push({"source": parseInt(i), "target": parseInt(n), "value": 1}) }
      }
    }).filter(function(d) { return typeof d !== "undefined"; });

    // draw links
    var link = svg.selectAll(".link")
        .data(links)
      .enter().append("line")
        .attr("class", "link")
        .attr("x1", function(d) { return nodes[d.source].x; })
        .attr("y1", function(d) { return nodes[d.source].y; })
        .attr("x2", function(d) { return nodes[d.target].x; })
        .attr("y2", function(d) { return nodes[d.target].y; })
        .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    // draw nodes
    var node = svg.selectAll(".node")
        .data(nodes)
      .enter().append("g")
        .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")"; }
        );

    var circle = node.append("circle")
        .attr("class", "node")
        .attr("r", nodeSize)
        .style("fill", function(d) { return color(d.layer); });


    node.append("text")
        .attr("dx", "-.35em")
        .attr("dy", ".35em")
        .text(function(d) { return d.label; });
});