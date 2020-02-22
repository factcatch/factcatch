let svg = d3.select('#source-relationship'),
    width = +svg.attr('width'),
    height = +svg.attr('height');

const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .on('zoom', zoomed);

const color = d3.scaleOrdinal(d3.schemeCategory20);
// const color = d3.scaleOrdinal(['black', '#ccc', '#ccc']);

const simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(d => d.id))
    .force('charge', d3.forceManyBody().strength(-80))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collisionForce', d3.forceCollide(22).strength(1).iterations(100).radius(40));

let circle;

let g = svg.append('g');

// const canId = document.currentScript.getAttribute('candidateId');
const api = `http://localhost:5019/keyword/relationships`;

// d3.json(api, (error, grap) => {
  // if (error) throw error;
  const graph = {
    "nodes": [
      {"id": "1", "group": 1},
      {"id": "2", "group": 2},
      {"id": "4", "group": 3},
      {"id": "8", "group": 4},
      {"id": "16", "group": 5},
      {"id": "11", "group": 1},
      {"id": "12", "group": 2},
      {"id": "14", "group": 3},
      {"id": "18", "group": 4},
      {"id": "116", "group": 5}
    ],
    "links": [
      {"source": "1", "target": "2", "value": 1},
      {"source": "2", "target": "4", "value": 1},
      {"source": "4", "target": "8", "value": 1},
      {"source": "4", "target": "8", "value": 1},
      {"source": "8", "target": "16", "value": 1},
      {"source": "16", "target": "1", "value": 1}
    ]
  }

  const link = g.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(graph.links)
        .enter()
        .append('line')
        .attr('stroke-width', (d) => Math.sqrt(d.value))
        .attr('class', (d) => { return toClass(`${d.source} ${d.target}`); });

  const node = g.append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(graph.nodes)
        .enter()
        .append('g');

  const weight = g.append('g')
        .attr('class', 'weights')
        .selectAll('text')
        .data(graph.links)
        .enter()
        .append('text')
        .text(d => d.value)
        .attr('fill', (d) => color(d.value))
        .attr('class', (d) => { return toClass(`${d.source} ${d.target}`); });

   circle = node.append('circle')
        .attr('r', (d) => d.freq)
        .attr('fill', (d) => {return "red";})
        .attr('class', (d) => { return toClass(d.id); })
        .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    node.append('text')
      .text((d) => d.id)
      .attr('class', (d) => { return toClass(d.id); })
      .attr('x', 6)
      .attr('y', 3);

    node.append('title')
      .text((d) => d.id);

    simulation
      .nodes(graph.nodes)
      .on('tick', ticked);

    simulation.force('link')
      .links(graph.links);

  function ticked() {
    link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y)
        

    node
        .attr('transform', (d) => 'translate(' + d.x + ',' + d.y + ')');

    weight
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2);
  }
// });

// g.call(d3.zoom()
//       .extent([[0, 0], [width, height]])
//       .scaleExtent([1, 8])
//       .on('zoom', zoomed));

//   function zoomed() {
//     // const {transform} = d3.event;
//     d = d3.event;
//     // circle.attr("transform", (d) => { return "translate(" + d.x + "," + d.y + ")";});
//   }

svg.call(zoom);

// delete option
let delOp = false;
let delBtn = d3.select('#del-relation-option');
let viewBtn = d3.select('#view-relation-option');

viewBtn.on('click', ()=>{
  delOp = false;
  delBtn.attr('class','btn btn-metal m-btn btn-sm m-btn--icon');
  viewBtn.attr('class','btn btn-warning m-btn btn-sm m-btn--icon');
})

delBtn.on('click', () => { 
    delOp = true;
    viewBtn.attr('class','btn btn-metal m-btn btn-sm m-btn--icon');
    delBtn.attr('class','btn btn-danger m-btn btn-sm m-btn--icon');
});
// end delete option

function dragstarted(d) {
  if (delOp) {
    d3.select(this).remove();
    d3.selectAll('.' + toClass(`${d.id}`)).remove();
    return;
  }
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function reset() {
  svg.transition().duration(750).call(
    zoom.transform,
    d3.zoomIdentity,
    d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
  );
}

function clicked(d) {
  const [[x0, y0], [x1, y1]] = path.bounds(d);
  d3.event.stopPropagation();
  svg.transition().duration(750).call(
    zoom.transform,
    d3.zoomIdentity
      .translate(width / 2, height / 2)
      .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
      .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
    d3.mouse(svg.node())
  );
}

function zoomed() {
  const { transform } = d3.event;
  g.attr('transform', transform);
  g.attr('stroke-width', 1 / transform.k);
}

function toClass(s) {
  // let ss = s.replace('.', '');
  // console.log('ss', ss);
  return s.replace('.', '');
}

