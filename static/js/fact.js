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

function selectClaim(index,claim){
  console.log(index);
  var itemClicked = document.getElementsByClassName("row-clicked");
  if (itemClicked.length != 0){
    itemClicked.item(0).classList.remove("row-clicked");
  }
  document.getElementById(claim["Claim_ID"]).classList.add("row-clicked");
  document.querySelector('input[type=hidden]').setAttribute("value",claim["Claim_ID"]);
  document.getElementById("no-claim").innerHTML = index + '.';
  document.getElementById("title-claim").innerHTML = claim.Claim;
  document.getElementById("origins-claim").innerHTML = claim["Origins"];
  document.getElementById("description-short").innerHTML = claim["Description"].substring(0,100);
  document.getElementById("more").innerHTML = claim["Description"].substring(100,);
  document.getElementById("example-claim").innerHTML = claim.Example;
  document.getElementById("originally-published-claim").innerHTML = claim["Originally Published"];
  document.getElementById("last-updated-claim").innerHTML = claim["Last Updated"];
  var tags = claim["Tags"];
  var i,tagHTML='';
  for (i=0;i<tags.length;i++){
      tagHTML += '<span class="tag-claim-item">#'+tags[i]+'</span>';
  }
  // for tag in tags:
  //   console.log(tag);
  document.getElementById("tag-claim").innerHTML = tagHTML; //claim["Tags"];
}

function get(route) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    }
  };
  url = "http://localhost:5050/" + route;
  console.log(url);
  xhttp.open("GET",url,true);
  xhttp.send();
}

function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
};

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
