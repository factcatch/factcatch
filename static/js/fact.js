// alert('fact');
function readMore() {
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("btn-readmore");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    moreText.style.display = "inline";
  }
}

var i_nextClaim = 0;

function selectClaim(index) {
  drawRelation(index);
  // console.log("Select claim data",claims[index]);
  // console.log("select map claim",index);
  var claim = claims[index];
  var itemClicked = document.getElementsByClassName("row-clicked");
  if (itemClicked.length != 0) {
    itemClicked.item(0).classList.remove("row-clicked");
  }
  document.getElementById(claim.id).classList.add("row-clicked");
  document.querySelector("input[type=hidden]").setAttribute("value", claim.id);
  // document.getElementById("title-claim-action-tab").innerHTML = claim.claim;
  // document.getElementById("no-claim").innerHTML = index + '.';
  // document.getElementById("title-claim").innerHTML = claim.Claim;
  document.getElementById("origins-claim").innerHTML = claim.origins;
  document.getElementById(
    "description-short"
  ).innerHTML = claim.description.substring(0, 100);
  document.getElementById("more").innerHTML = claim.description.substring(100);
  document.getElementById("example-claim").innerHTML = claim.example;
  document.getElementById("originally-published-claim").innerHTML =
    claim.originally_published;
  document.getElementById("last-updated-claim").innerHTML = claim.last_updated;
  var tags = claim.tags;
  var i,
    tagHTML = "";
  for (i = 0; i < tags.length; i++) {
    tagHTML += '<span class="tag-claim-item">#' + tags[i] + "</span>";
  }
  i_nextClaim = index + 1;
  // for tag in tags:
  //   console.log(tag);
  document.getElementById("tag-claim").innerHTML = tagHTML; //claim["Tags"];
}

function nextToClaim(){
  selectClaim(i_nextClaim);
}

function get(route) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    }
  };
  url = "http://localhost:5050/" + route;
  xhttp.open("GET", url, true);
  xhttp.send();
}

function selectTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tab-main-content");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  // document.getElementById(tabName).style.display = "block";
  activedTabs = document.getElementsByClassName(tabName);
  for (i = 0; i < activedTabs.length; i++) {
    activedTabs[i].style.display = "block";
  }
  evt.currentTarget.className += " active";
  console.log("evt",evt);
}

function openTabClaim(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabclaims");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinkclaims");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  
  evt.currentTarget.className += " active";
}

function drawRelation(index) {
  var claim = claims[index];
  d3.select(".chart-sources-claim > svg").remove();

  var sources = claim.documents;
  var data = sources; //JSON.parse(sources);

  var outer = d3.map();
  var inner = [];
  var links = [];
  var outerId = [0];

  data.forEach(function(d) {
    if (d == null) return;

    i = {
      id: "i" + inner.length,
      name: d[0],
      content: d[1],
      related_links: []
    };
    i.related_nodes = [i.id];
    inner.push(i);

    if (!Array.isArray(d[2])) d[2] = [d[2]];

    d[2].forEach(function(d1) {
      o = outer.get(d1);

      if (o == null) {
        o = { name: d1, id: "o" + outerId[0], related_links: [] };
        o.related_nodes = [o.id];
        outerId[0] = outerId[0] + 1;

        outer.set(d1, o);
      }

      // create the links
      l = { id: "l-" + i.id + "-" + o.id, inner: i, outer: o };
      links.push(l);

      // and the relationships
      i.related_nodes.push(o.id);
      i.related_links.push(l.id);
      o.related_nodes.push(i.id);
      o.related_links.push(l.id);
    });
  });

  data = {
    inner: inner,
    outer: outer.values(),
    links: links
  };

  // sort the data -- TODO: have multiple sort options
  outer = data.outer;
  data.outer = Array(outer.length);

  var i1 = 0;
  var i2 = outer.length - 1;

  for (var i = 0; i < data.outer.length; ++i) {
    if (i % 2 == 1) data.outer[i2--] = outer[i];
    else data.outer[i1++] = outer[i];
  }

  console.log(
    data.outer.reduce(function(a, b) {
      return a + b.related_links.length;
    }, 0) / data.outer.length
  );

  // from d3 colorbrewer:
  // This product includes color specifications and designs developed by Cynthia Brewer (http://colorbrewer.org/).
  var colors = [
    "#a50026",
    "#d73027",
    "#f46d43",
    "#fdae61",
    "#fee090",
    "#ffffbf",
    "#e0f3f8",
    "#abd9e9",
    "#74add1",
    "#4575b4",
    "#313695"
  ];
  // var colors = ["#001f3f","#0074D9","#7FDBFF","#39CCCC","#3D9970","#2ECC40","#01FF70","#FFDC00","#FF851B","#FF4136","#F012BE"]
  // var colors = d3.scaleQuantize()
  //     .domain([100, 200])
  //     .range(["#5E4FA2", "#3288BD", "#66C2A5", "#ABDDA4", "#E6F598",
  //         "#FFFFBF", "#FEE08B", "#FDAE61", "#F46D43", "#D53E4F", "#9E0142"]);
  var color = d3.scale
    .linear()
    .domain([10, 220])
    .range([colors.length - 1, 0])
    .clamp(true);

  // var diameter = 960;
  // var diameter = 1960;
  var diameter = 1000; //document.getElementById('content-claim').offsetWidth;
  // console.log("char width",diameter);
  var rect_width = 160;
  var rect_height = 20;

  var link_width = "1px";

  var il = data.inner.length;
  var ol = data.outer.length;

  var inner_y = d3.scale
    .linear()
    .domain([0, il])
    .range([-(il * rect_height) / 2, (il * rect_height) / 2]);

  mid = data.outer.length / 2.0;
  var outer_x = d3.scale
    .linear()
    .domain([0, mid, mid, data.outer.length])
    .range([15, 170, 190, 355]);

  var outer_y = d3.scale
    .linear()
    .domain([0, data.outer.length])
    .range([0, diameter / 2 - 120]);

  // setup positioning
  data.outer = data.outer.map(function(d, i) {
    d.x = outer_x(i);
    d.y = diameter / 3;
    return d;
  });

  data.inner = data.inner.map(function(d, i) {
    d.x = -(rect_width / 2);
    d.y = inner_y(i);
    return d;
  });

  function get_color(name) {
    var c = Math.round(color(name));
    if (isNaN(c)) return "#dddddd"; // fallback color

    return colors[c];
  }

  // Can't just use d3.svg.diagonal because one edge is in normal space, the
  // other edge is in radial space. Since we can't just ask d3 to do projection
  // of a single point, do it ourselves the same way d3 would do it.

  function projectX(x) {
    return ((x - 90) / 180) * Math.PI - Math.PI / 2;
  }

  var diagonal = d3.svg
    .diagonal()
    .source(function(d) {
      return {
        x: d.outer.y * Math.cos(projectX(d.outer.x)),
        y: -d.outer.y * Math.sin(projectX(d.outer.x))
      };
    })
    .target(function(d) {
      return {
        x: d.inner.y + rect_height / 2,
        y: d.outer.x > 180 ? d.inner.x : d.inner.x + rect_width
      };
    })
    .projection(function(d) {
      return [d.y, d.x];
    });

  var svg = d3
    .select(".chart-sources-claim")
    .append("svg")
    .attr("viewBox", [0, 0, diameter, diameter]);
    // .attr("width", diameter)
    // .attr("height", diameter)

  const g = svg .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

    svg.call(d3.zoom()
    .extent([[0, 0], [diameter, diameter]])
    .scaleExtent([1, 8])
    .on("zoom", zoomed));

    function zoomed() {
      g.attr("transform", d3.event.transform);
    }

  // links
  var link = g
    .append("g")
    .attr("class", "links")
    .selectAll(".link")
    .data(data.links)
    .enter()
    .append("path")
    .attr("class", "link")
    .attr("id", function(d) {
      return d.id;
    })
    .attr("d", diagonal)
    .attr("stroke", function(d) {
      return "gray"; /*get_color(d.inner.name);*/
    })
    .attr("stroke-width", link_width);

  // outer nodes

  var onode = g
    .append("g")
    .selectAll(".outer_node")
    .data(data.outer)
    .enter()
    .append("g")
    .attr("class", "outer_node")
    .attr("transform", function(d) {
      return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")";
    })
    .on("mouseover", mouseover)
    .on("mouseout", mouseout);

  onode
    .append("circle")
    .attr("id", function(d) {
      return d.id;
    })
    .attr("r", 6.5);

  onode
    .append("circle")
    .attr("r", 20)
    .attr("visibility", "hidden");

  onode
    .append("text")
    .attr("id", function(d) {
      return d.id + "-txt";
    })
    .attr("dy", ".31em")
    .attr("text-anchor", function(d) {
      return d.x < 180 ? "start" : "end";
    })
    .attr("transform", function(d) {
      return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)";
    })
    .text(function(d) {
      return d.name;
    });

  // inner nodes

  var inode = g
    .append("g")
    .selectAll(".inner_node")
    .data(data.inner)
    .enter()
    .append("g")
    .attr("class", "inner_node")
    .attr("transform", function(d, i) {
      return "translate(" + d.x + "," + d.y + ")";
    })
    .on("mouseover", mouseover)
    .on("mouseout", mouseout)
    .append("a")
    .attr("target", "_blank")
    .attr("href", function(d) {
      return "https://" + d.content;
    });

  inode
    .append("rect")
    .attr("width", rect_width)
    .attr("height", rect_height)
    .attr("id", function(d) {
      return d.id;
    })
    .attr("fill", function(d) {
      return get_color(d.name);
    });

  inode
    .append("text")
    .attr("id", function(d) {
      return d.id + "-txt";
    })
    .attr("text-anchor", "middle")
    .attr(
      "transform",
      "translate(" + rect_width / 2 + ", " + rect_height * 0.75 + ")"
    )
    .text(function(d) {
      return d.content;
    });

  // need to specify x/y/etc

  d3.select(self.frameElement).style("height", diameter - 150 + "px");

  function mouseover(d) {
    // bring to front
    d3.selectAll(".links .link").sort(function(a, b) {
      return d.related_links.indexOf(a.id);
    });

    for (var i = 0; i < d.related_nodes.length; i++) {
      d3.select("#" + d.related_nodes[i]).classed("highlight", true);
      d3.select("#" + d.related_nodes[i] + "-txt").attr("font-weight", "bold");
    }

    for (var i = 0; i < d.related_links.length; i++)
      d3.select("#" + d.related_links[i])
        .attr("stroke-width", "4px")
        .attr("stroke", "#0da4d3");
  }

  function mouseout(d) {
    for (var i = 0; i < d.related_nodes.length; i++) {
      d3.select("#" + d.related_nodes[i]).classed("highlight", false);
      d3.select("#" + d.related_nodes[i] + "-txt").attr(
        "font-weight",
        "normal"
      );
    }

    for (var i = 0; i < d.related_links.length; i++)
      d3.select("#" + d.related_links[i])
        .attr("stroke-width", link_width)
        .attr("stroke", "gray");
  }
}

function randomColor() {
  var colors = [
    "#a50026",
    "#d73027",
    "#f46d43",
    "#fdae61",
    "#fee090",
    "#ffffbf",
    "#e0f3f8",
    "#abd9e9",
    "#74add1",
    "#4575b4",
    "#313695"
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}

function sourceClick() {
  this.classList.toggle("active");
  var content = this.nextElementSibling;
  if (content.style.maxHeight) {
    content.style.maxHeight = null;
  } else {
    content.style.maxHeight = content.scrollHeight + "px";
  }
}

function selectMode(mode) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("listcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  document.getElementById(mode.value).style.display = "block";
  // evt.currentTarget.className += " active";
}

function changeMode(mode) {
  selectMode(mode.value);
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
document.getElementById("defaultDetails").click();

var coll = document.getElementsByClassName("source-item");
var i;

var chartImg = false;
$("#toggle-overview").click(function() {
  $("#chart-overview").toggle();
  chartImg = !chartImg;
  if (chartImg) {
    $("#overview").css({ height: "90px" });
    $("#analysis").css({
      "grid-column-start": "1",
      "grid-column-end": "3",
      "grid-template-columns": "auto auto auto auto",
      padding: "0px",
      "margin-top" : "0px",
      height: ""
    });
    // $("#toggle-overview").css({"margin-top":"15px"});
    document.getElementById("icon-toggle-overview").classList.remove("fa-chevron-up");
    document.getElementById("icon-toggle-overview").classList.add("fa-chevron-down");
    $("#toggle-overview").css({ top: "20px" });
  } else {
    $("#overview").css({ height: "" });
    $("#analysis").css({
      "grid-column-start": "",
      "grid-column-end": "",
      "grid-template-columns": "auto auto",
      height: "200px",
      "margin-top" : "80px",
    });
    $("#toggle-overview").css({ top: "270px" });
    // $("#toggle-overview").css({"margin-top":"220px"});
    document.getElementById("icon-toggle-overview").classList.remove("fa-chevron-down");
    document.getElementById("icon-toggle-overview").classList.add("fa-chevron-up");
  }
});
function filterSource() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("input-sourceFilter");
  filter = input.value.toUpperCase();
  table = document.getElementById("heatmap-sources");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
              tr[i].style.display = "";
          } else {
              tr[i].style.display = "none";
          }
      }
  }
}

// chart for overview checking
