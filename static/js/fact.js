// alert('fact');
var claims = [];
updateListClaim('');

const status_question = {
  QUESTION : 'question',
  VALIDATING : 'loading',
  AFTER : 'validated'
}

const rank_mode = {
  BY_PROB_MODEL : 0,
  BY_CREDIBLE : 1,
  BY_RANDOM : 2,
}

function triggerMatrix(mode){
  document.getElementById('fact-checking-body')
    .style.display = (mode == 0) ? '' : 'none';
  document.getElementById('matrix-factorization')
    .style.display =  (mode==1) ? '' : 'none';
}


function setStatusQuestion(mode){
  document.getElementById('question-validate').style = (mode == status_question.QUESTION) ? 'display:inline-block' : 'display:none';
  document.getElementById('loading-validate-claim').style = (mode == status_question.VALIDATING) ? 'display:inline-block' : 'display:none';
  document.getElementById('after-validated').style = (mode == status_question.AFTER) ? 'display:inline-block' : 'display:none';
  document.getElementById('block-list-claim').style = (mode == status_question.VALIDATING)  ? 'opacity: 0.2' : 'opacity:';
  document.getElementById('detail-source').style = (mode == status_question.VALIDATING)  ? 'opacity: 0.4' : 'opacity:';
}

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

function findIndexClaimById(claim_id) {
  let index_ = 0;
  claims.forEach(function(item, index) {
    if (item.id === claim_id) {
      index_ = index;
    }
  });
  return index_;
}

function selectClaim(index) {
  // drawRelation(index);
  // document.getElementById("input_claim_id_for_form").setAttribute
  var claim = claims[index];
  drawNeuralNetwork(claim.id);
  let status_ = (claim.credibility == -1) ? status_question.QUESTION : status_question.AFTER; 
  setStatusQuestion(status_);
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

function nextToClaim() {
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

  const g = svg
    .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

  svg.call(
    d3
      .zoom()
      .extent([
        [0, 0],
        [diameter, diameter]
      ])
      .scaleExtent([1, 8])
      .on("zoom", zoomed)
  );

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
    .on("mouseout", mouseout)
    .on("click", nodeClick);

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

  function nodeClick(d) {
    let index_claim = findIndexClaimById(d.name[0]);
    selectClaim(index_claim);
    scrollToClaim(d.name[0]);
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
      "margin-top": "0px",
      height: ""
    });
    // $("#toggle-overview").css({"margin-top":"15px"});
    document
      .getElementById("icon-toggle-overview")
      .classList.remove("fa-chevron-up");
    document
      .getElementById("icon-toggle-overview")
      .classList.add("fa-chevron-down");
    $("#toggle-overview").css({ top: "20px" });
  } else {
    $("#overview").css({ height: "" });
    $("#analysis").css({
      "grid-column-start": "",
      "grid-column-end": "",
      "grid-template-columns": "auto auto",
      height: "200px",
      "margin-top": "80px"
    });
    $("#toggle-overview").css({ top: "270px" });
    // $("#toggle-overview").css({"margin-top":"220px"});
    document
      .getElementById("icon-toggle-overview")
      .classList.remove("fa-chevron-down");
    document
      .getElementById("icon-toggle-overview")
      .classList.add("fa-chevron-up");
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

// source map 

var sourcesHeatmap,fullSources,batchData,batchClaim = [],fullClaims=claims;

function showInfoSource(source) {
  document.getElementById("title-source-item").innerHTML = source.source;
  document.getElementById("total-claim-source-item").innerHTML = source.total;
  document.getElementById("source-credibility-progress").style.width = ((source.credibility * 100)/(source.credibility + source.uncredibility)).toFixed(2) + '%' ;
  document.getElementById("credibility-per").innerHTML =  ((source.credibility * 100)/(source.credibility + source.uncredibility)).toFixed(2) + '%' ;
};

function renderHeatmap(){ 
  if(batchData !== undefined){
    batchClaim = [];
    let cache = fullSources.filter(function(e){
      return batchData.includes(e.source);
    });
    sourcesHeatmap = JSON.parse(JSON.stringify(cache));
    sourcesHeatmap.map(function(e,i){
      e.claims = [...e.claims.filter(function(c){
        return batchData.includes(c.claim_id);
      })];
      e.claims.map(function(c,i){
        batchClaim.push(c.claim_id);
      })
    });
  }
  var marginChartOverview = { top: 30, right: 30, bottom: 30, left: 50 },
            widthChartOverview = $(window).width() * 0.75 - 30 - marginChartOverview.left - marginChartOverview.right,
            heightChartOverview = 250 - marginChartOverview.top - marginChartOverview.bottom;

  let loader = d3.select("#loader-source");
  d3.select("table").html('');
  loader.style("display","none");
  var table = d3.select("table")
      .selectAll("tr")
      .data(sourcesHeatmap)
      .enter()
      .append("tr")
  table.append("td")
      .text(function (d) { return d.source })
      .style("text-align", "right")

  table.append("td")
      .attr("id", function (d) { return d.source.replace(/\./g, '') })
      .style("text-align", "left")
  // showInfoSource(data[0]);
  sourcesHeatmap.map((source) => {
      var widthCell = 20, heightCell = 20, p = 20,maxClaims = 30;
      p = Math.floor(($(window).width() * 0.7 - 100 - marginChartOverview.left - marginChartOverview.right) / 20);
      var width = widthCell * maxClaims; //source.claims.length;
      var height = heightCell * Math.ceil(source.claims.length / maxClaims);
      // var data = data[0];

      // append the svg object to the body of the page
      var sourceId = '[id="' + source.source.replace(/\./g, '') + '"]';
      var svg = d3.select(sourceId)
          .append("svg")
          .attr("width", width)
          .attr("height", height)


      // var colorClaim = d3.scaleLinear().domain([1, 10])
          // .range(["#a9a9a9", "rgb(237,105,37)"])

      var colorClaim = d3.scaleOrdinal().domain([-1, 1])
          // .range(["grey","#1dc9b7","#fd397a"])
          // .range(["grey","#66BC6D","#D20D01"])
          .range(["grey","#6ACB44","#F72A38"])


      var tooltip = d3.select("#all-sources")
          .append("div")
          .style("opacity", 0)
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("border", "solid")
          .style("border-width", "2px")
          .style("border-radius", "5px")
          .style("padding", "5px")
          .style("position", "fixed")
          .style("max-width", "350px")
      // .style("margin-top", "20px")


      // Three function that change the tooltip when user hover / move / leave a cell
      var mouseover = function (d) {
          tooltip
              .style("opacity", 1)
          d3.select(this)
              .style("stroke", "black")
              .style("opacity", 1)
          showInfoSource(source);
      }
      var mousemove = function (d) {
          var mouseTop = d3.mouse(this)[1] < 300 ? d3.mouse(this)[1] + 300 : d3.mouse(this)[1];
          var mouseTop = (d3.mouse(this)[1] % 10) + 350;
          tooltip
              .html(d.claim)
              .style("left", (d3.mouse(this)[0] + 200) + "px")
              .style("top", (mouseTop) + "px")
      }
      var mouseleave = function (d) {
          tooltip
              .style("opacity", 0)
          d3.select(this)
              .style("stroke", "white")
              .style("opacity", 0.8)
      }

      var rectClick = function (d) {
          document.getElementById('tab-claims').click();
          selectClaim(findIndexClaimById(d.claim_id));
          scrollToClaim(d.claim_id);
      }

      svg.selectAll("rect")
          .data(source.claims)
          .enter()
          .append("rect")
          .attr("x", function (d, i) { return widthCell * ((i%maxClaims) % p); })
          .attr("y", function (d, i) { return heightCell * (Math.floor((i/maxClaims))); })
          .attr("width", "20")
          .attr("height", "20")
          .style("fill", function (d) { return colorClaim(d.credibility_claim); })
          .style("stroke-width", 1)
          .style("stroke", "white")
          .style("opacity", 0.8)
          .on("mouseover", mouseover)
          .on("mousemove", mousemove)
          .on("mouseleave", mouseleave)
          .on("click", rectClick);

      // append text to rect
      svg.selectAll("text")
          .data(source.claims)
          .enter()
          .append("text")
          .attr("x", function (d, i) { return widthCell * ((i%maxClaims) % p) + widthCell/3; })
          .attr("y", function (d, i) { return heightCell * (Math.floor((i/maxClaims))) + heightCell/1.5; })
          .style("fill", function (d) { return "#fff"; })
          .text(function(d) { return d.credibility_claim == -1 ? '?' : ''});
  });
}

function renderSources() {
        let loader = d3.select("#loader-source");
        loader.style("display","inline-block");
        d3.select("table").html('');

        var table = d3.select("table");
        d3.json("http://localhost:5050/source/claim", function (data) {
            sourcesHeatmap = data;
            fullSources = Array.from(data);
            renderHeatmap();
        })
}

function filterForHeatmap(e){
  // console.log("full sources before",fullSources);
  // console.log("full claims before",fullClaims);
  batchData = Array.from(e.map(function(val,index){
    // console.log(val.getAttribute("data"));
    return val.getAttribute("data");
  }));
  console.log("batch Data",batchData);
  renderHeatmap();
  sortListClaim();
  // renderListClaim();
  triggerMatrix(0);
  // console.log("full sources after",fullSources);
  // console.log("full claims after",fullClaims);
}

// validate claim

function renderListClaim(){
  // console.log('render list claim',claims);
  d3.select("#list-claim").html('');
  d3.select("#list-claim")
  .selectAll("li")
  .data(claims)
  .enter()
  .append("li")
  .attr("id",function(d){return d.id;})
  .attr("onclick",function(d,i){return 'selectClaim(' +i+')';})
  .style('display',function(d){return d.credibility >= 0 ? 'grid' : ''})
  .style('grid-template-columns',function(d){return d.credibility >=0 ? 'auto 35px' : ''})
  .html(function(d, i) {
    let width_progressbar = d.prob_model * 100;
    let bg_progressbar = (d.prob_model >= 0.5) ? '#6ACB44' : '#F72A38';
    let level = (d.prob_model*100).toFixed(2);
    // let style_validated = (d.credibility >= 0) ? 'style="display: grid;grid-template-columns:auto 35px;" ' : '';
    let title = `
      <div class="title-claim">
            <span class="no-claim">` + (i + 1) + `. </span> 
            <span>` + d.claim + `</span> 
      </div>
    `;
    let validated_claim = (d.credibility == 1) ? 
    `
      <div style="padding: 75% 8px;">
        <img src="../img/credit.png" width="24px"
        style="opacity: 0.5;">
      <div>
    ` : 
    `
      <div style="padding: 75% 8px;">
          <img src="../img/danger2.png" width="24px"
            style="opacity: 0.5;">
      </div>
    `;
    let non_validated_claim = `
      <div class="progressbar" style="padding: 0;">
            <div
                style="width: ` + width_progressbar + `%; opacity:0.8; background-color:`+ bg_progressbar+ `">
            </div>
        </div>
        <div class="detail-progressbar-credi" style="padding: 4px 0px;font-size: 12px;">
            <div class="percentage-credib">
              Credibility
            </div>
            <div class="percentage-progressbar-credi">
              ` +level +  `%
            </div>
        </div>
    `;
    let html = title + (d.credibility >= 0 ? validated_claim : non_validated_claim);
    return html; //'<span class="no-claim"> ' + (i+1) + '. </span>' + d.id;
  });
}

function scrollToClaim(claim_id){
  let claim = document.getElementById(claim_id);
  claim.scrollIntoView(true);
}

function updateListClaim(claim_id_for_update) {
  if(claim_id_for_update === ''){
    document.getElementById('block-content2').style.display = 'none';
    document.getElementById('loader-claim').style.display = '';
  }
  d3.json("http://localhost:5050/claim/getAllClaims", function(err, res) {
    if(claim_id_for_update === ''){
      document.getElementById('loader-claim').style.display = 'none';
      document.getElementById('block-content2').style.display = 'grid';
    }
    claims = Array.from(res);
    fullClaims = Array.from(claims);
    sortListClaim();
    // renderListClaim();
    let index_ = findIndexClaimById(claim_id_for_update)
    selectClaim(index_);
    scrollToClaim(claim_id_for_update === '' ? claims[0].id : claim_id_for_update);
    if(document.getElementById('loading-validate-claim').innerHTML == 'Invalidating')
      document.getElementById('loading-validate-claim').innerHTML = 'Validating claim';
  });
}

function updateOverview(){
  d3.json('http://localhost:5050/claim/getAnalysis',function(err,data){
      // document.getElementById('total-claim-detail_').innerHTML = data.claims
      document.getElementById('remain-claim-source-item').innerHTML = (data.claims - data.credibility - data.nonCredibility) + ' ('  + data.perNonValidated + '%)';
      document.getElementById('credit-claim_').innerHTML = data.credibility + ' (' + data.perCred + '%)';
      document.getElementById('noncredit-claim_').innerHTML = data.nonCredibility + ' (' + data.perNonCred + '%)';
      document.getElementById('uncertainty').innerHTML = data.uncertainty;
  });
}

function validateClaim(c) {
  var claim_id_for_update = document.getElementById("input_claim_id_for_form").value
  claim = {
    id: claim_id_for_update,
    credible: c
  };
  if(c==-1)
    document.getElementById("loading-validate-claim").innerHTML = "Invalidating";
  setStatusQuestion(status_question.VALIDATING);
  d3.request("http://localhost:5050/claim/validate")
    .header("Content-Type", "application/json")
    .post(JSON.stringify(claim), function(){
      updateListClaim(claim_id_for_update);
      updateOverview();
      drawModelProb();
      renderSources();
    });
}

function drawModelProb(){
  d3.select("#chart-overview").html('');
  d3.json("http://localhost:5050/claim/getHistogram", function (data) {
          d3.select("#chart-overview").html(
            '<canvas id="myChart" width="600" height="600"></canvas>'
          );
          let min = 10000000,max=-1;
          data.histogram.forEach(function(e){
            max = Math.max(e,max);
            min = Math.min(e,min);
          });
          var colorBar = d3.scaleLinear()
                .domain([min,max])
                .range(["#84c2f4","#1a80ce"])
          var ctx = document.getElementById("myChart").getContext('2d');
          ctx.canvas.parentNode.style.height = '340px';
          ctx.canvas.parentNode.style.width = '380px';
            var myChart = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
                datasets: [{
                  label: '#Claims',
                  data: data.histogram,
                  backgroundColor: [
                    colorBar(data.histogram[0]),
                    colorBar(data.histogram[1]),
                    colorBar(data.histogram[2]),
                    colorBar(data.histogram[3]),
                    colorBar(data.histogram[4])
                    // "#1a80ce"
                    // '#4ca7e8',
                    // '#84c2f4',
                    // '#39a3ef',
                    // '#3d9ce5'
                  ],
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                title: {
                  display: true,
                  text: 'Credibility Histogram'
                },
                scales: {
                  xAxes: [{
                    barPercentage: 0.8,
                    ticks: {
                      maxRotation: 90,
                      minRotation: 80
                    }
                  }],
                  yAxes: [{
                    ticks: {
                      beginAtZero: true
                    }
                  }]
                }
              }
            });
  });

    // d3.json("http://localhost:5050/claim/getUserCredAndModel", function (data) {
    //   d3.select("#chart-overview > div > canvas").html('');
    //   let lables_ = [...Array(Object.keys(data.modelProb).length).keys()];
    //   lables_.map(function(val,index) {
    //       lables_[index] = val + 1;
    //   });
    //   var config = {
    //       type: 'line',
    //       data: {
    //           labels: lables_,
    //           datasets: [{
    //               label: 'Model Probability',
    //               fillColor: "rgba(220,220,220,0.2)",
    //               strokeColor: "rgba(220,220,220,1)",
    //               // backgroundColor: window.chartColors.red,
    //               borderColor: 'rgba(151,187,205,1)',
    //               data: data.modelProb,
    //           }],
    //       },
    //       options: {
    //           responsive: true,
    //           title: {
    //               display: true,
    //               text: 'Comparison Model and User Input'
    //           },
    //           scales: {
    //               xAxes:
    //                   [{
    //                       ticks: {
    //                           autoSkip: true,
    //                           maxTicksLimit: 5,
    //                       }
    //                   }],
    //               yAxes: [{
    //                   ticks: {
    //                       autoSkip: true,
    //                       maxTicksLimit: 5,
    //                   }
    //               }]
    //           }
    //       }
    //   };
    //   var ctx = document.getElementById('canvas').getContext('2d');
    //   window.myLine = new Chart(ctx, config);
    // });
}


function sortListClaim() {
    let ranking = document.getElementById('ranking-select');
    let sort_by = ranking.options[ranking.selectedIndex].value;
    let mode = parseInt(sort_by);
    if(batchClaim.length > 0)
      claims = Array.from(fullClaims.filter(function(e){
        return batchClaim.includes(e.id);
      }));
    let claims_by_prob_model = [];
    let credible_claims = [];
    let non_credible_claim = [];
    claims.map(function(val,key){
      switch (val.credibility) {
        case 1:
          credible_claims.push(val);
          break;
        case 0:
          non_credible_claim.push(val);
          break;
        default:
          claims_by_prob_model.push(val);
          break;
      }
    });
    let claims_ = new Array();
    switch (mode) {
      case rank_mode.BY_CREDIBLE:
        claims_by_prob_model.sort(function(a,b){
          return b.prob_model - a.prob_model;
        });
        claims_ = claims_.concat(credible_claims);
        claims_ = claims_.concat(claims_by_prob_model);
        claims_ = claims_.concat(non_credible_claim);
        claims = Array.from(claims_);
        break;
      case rank_mode.BY_RANDOM:
        var currentIndex = claims.length, temporaryValue, randomIndex;
        while (0 !== currentIndex) {
          randomIndex = Math.floor(Math.random() * currentIndex);
          currentIndex -= 1;
          temporaryValue = claims[currentIndex];
          claims[currentIndex] = claims[randomIndex];
          claims[randomIndex] = temporaryValue;
        }
        break;
      default:
        claims_by_prob_model.sort(function(a,b){
          let entropy_a =  - a.prob_model*Math.log(a.prob_model) - (1-a.prob_model)*Math.log(1-a.prob_model);
          let entropy_b =  - b.prob_model*Math.log(b.prob_model) - (1-b.prob_model)*Math.log(1-b.prob_model); 
          return entropy_b - entropy_a;
        });
        claims_ = claims_.concat(claims_by_prob_model);
        claims_ = claims_.concat(credible_claims);
        claims_ = claims_.concat(non_credible_claim);
        claims = Array.from(claims_);
        break;
    }
    // claims = Array.from(claims_);
    renderListClaim();
    selectClaim(0);
    scrollToClaim(claims[0].id);
}


function drawNeuralNetwork(claim_id){
  d3.select("#svg-neural-network").html('');
  var diameter = 800;

  var svg = d3
    .select("#svg-neural-network")
    .attr("viewBox", [0, 0, diameter, diameter]);
  // .attr("width", diameter)
  // .attr("height", diameter)
  var width = +svg.attr("width"), 
  height = +svg.attr("height")

  const g = svg
    .append("g")
    .attr("transform", "translate(" + diameter*0 / 2 + "," + diameter *0/ 2 + ")");
  
    // zoom
    svg.call(
      d3
        .zoom()
        .extent([
          [0, 0],
          [diameter, diameter]
        ])
        .scaleExtent([1, 8])
        .on("zoom", zoomed)
    );
  
    function zoomed() {
      g.attr("transform", d3.event.transform);
    }
  // svg = g;

  let api =  "http://localhost:5050/claim/getNeural?id=" + claim_id;

        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }))
            //.force("charge", d3.forceManyBody().strength(-200))
            .force('charge', d3.forceManyBody()
              .strength(-3000)
              .theta(0.8)
            //   .distanceMin(100)
              .distanceMax(150)
            )
        // 		.force('collide', d3.forceCollide()
        //       .radius(d => 40)
        //       .iterations(2)
        //     )
            .force("center", d3.forceCenter(width / 2, height / 2));
        var colors = [
          // "#99CB8A",
          "#D2849E",
          "#CFEB8A",
          "#D0D0FF",
          "#CA8DAD",
          // "#D1B897",
          // "#85E982",
          // "#E6DE95",
          // "#c0392b",
          "#e0f3f8",
          "#abd9e9",
          "#74add1",
          "#4575b4",
          "#FDAE61",
          // "#D73027"
        ]

        var color = d3.scaleLinear()
            .domain([0, 100])
            .range([colors.length - 1, 0])
            .clamp(true);

        function get_color(name) {
            var c = Math.round(color(name));
            if (isNaN(c)) return "#dddddd"; // fallback color

            return colors[c];
          }

        var colorClaim = d3.scaleOrdinal().domain([-1, 1])
          // .range(["grey","#6ACB44","#F72A38"])
          .range(["grey","#77C458","#F7535F"])


          
        function run(graph) {
          
          // graph.links.forEach(function(d){
        //     d.source = d.source_id;    
        //     d.target = d.target_id;
          // });           

          var link = g.append("g")
                        .attr("class", "links")
                        .style("stroke", "#666")
                        .selectAll("line")
                        .data(graph.links)
                        .enter().append("line")
                        .attr('id',function(d){return d.source + '' + d.target + '' + d.value;})
                        .style("stroke",function(d){ return "#333333"/*get_color(d.value)*/;})
                        .style("stroke-width",function(d) { return d.value / 200 + 'px'});

          var node = g.append("g")
                    .attr("class", "nodes")
                    .selectAll("circle")
                              .data(graph.nodes.filter(function(e){
                                return e.category == "source";
                              }))
                    .enter().append("circle")
                            .attr("r", 2)
                            .call(d3.drag()
                                .on("start", dragstarted)
                                .on("drag", dragged)
                                .on("end", dragended));

          var nodeClaim = g.append("g")
                .attr("class","nodes")
                .selectAll("rect")
                    .data(graph.nodes.filter(function(e){
                      return e.category == "claim";
                    }))
                .enter().append("rect")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
                    
          
          var label = g.append("g")
              .attr("class", "labels")
              .selectAll("text")
              .data(graph.nodes)
              .enter().append("text")
                .attr("class", "label")
                // .style("fill",'red')
                .text(function(d) { return d.name; })

          simulation
              .nodes(graph.nodes)
              .on("tick", ticked);

          simulation.force("link")
              .links(graph.links);
          
          function getSizeSource(d){
            if(d.group < 6){
              return (d.group + 6)*2;
            }
            return d.group > 40 ?  d.group / 2 : d.group*2; 
          }
          

          function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("r", function(d){ return d.category == 'source' ? getSizeSource(d) : 6})
                .style("fill", function(d){return d.category == 'source' ? get_color(d.group) : colorClaim(d.group)})
                .style("stroke", "#333")
                .style("stroke-width", "1.0px")
                .on("mouseover", mouseover)
                .on('mouseout',mouseout)
                .on("click", nodeClick)
                .attr("cx", function (d) { return d.x+5; })
                .attr("cy", function(d) { return d.y-3; });

            nodeClaim
                .attr("rx",2)
                .attr("ry",2)
                .attr("width",12)
                .attr("height",12)
                .attr("style","fill: rgb(106, 203, 68); stroke-width: 1; stroke: #333;")
                .style("fill",function(d){return colorClaim(d.group);})
                .on("mouseover", mouseover)
                .on('mouseout',mouseout)
                .on("click", nodeClick)
                .attr("x",function(d){return d.x - 2;})
                .attr("y",function(d){return d.y - 3;});
            
            label
                .attr("x", function(d) { return d.x; })
                    .attr("y", function (d) { return d.y; })
                    .style("font-size",function(d){ return d.category == "source" ? '18px' : '8px'})
                    .style("font-weight", function(d){ return d.category == "source" ? '500' : '300'})
                    .style("fill", function(d){return d.category == "source" ? "#DB1430" : "#44444"});
          }

          function mouseover(d) {
            for (var i = 0; i < graph.links.length; i++)
              if(d.id == graph.links[i].source.id || d.id == graph.links[i].target.id){
                d3.select('[id="' + graph.links[i].source.id + '' + graph.links[i].target.id +'' + graph.links[i].value + '"]')
                  .style("stroke-width", "1px")
                  .style("stroke", "#0da4d3");
              }
          }
        
          function mouseout(d) {
            for (var i = 0; i < graph.links.length; i++)
            if(d.id == graph.links[i].source.id || d.id == graph.links[i].target.id){
              d3.select('[id="' + graph.links[i].source.id + '' + graph.links[i].target.id +'' + graph.links[i].value + '"]')
                .style("stroke-width", '0.2px')
                .style("stroke", "#999999");
            }
          }

          function nodeClick(d) {
            if(d.category == "claim"){
              let index_claim = findIndexClaimById(d.name);
              selectClaim(index_claim);
              // console.log(d.name);
              scrollToClaim(d.name);
            } else {
              window.open("https://" + d.name);
            }
          }
        }

        function dragstarted(d) {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        //  simulation.fix(d);
        }

        function dragged(d) {
          d.fx = d3.event.x
          d.fy = d3.event.y
        //  simulation.fix(d, d3.event.x, d3.event.y);
        }

        function dragended(d) {
          d.fx = d3.event.x
          d.fy = d3.event.y
          if (!d3.event.active) simulation.alphaTarget(0);
          //simulation.unfix(d);
        }
          
    d3.json(api, function(err,data) {
        run(data);
    });
}

