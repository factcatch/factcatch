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
  // document.getElementById(claim["Claim_ID"]).classList.add("row-clicked");
  document.querySelector('input[type=hidden]').setAttribute("value",claim["Claim_ID"]);
  document.getElementById("no-claim").innerHTML = index + '.';
  document.getElementById("title-claim").innerHTML = claim.Claim;
  document.getElementById("origins-claim").innerHTML = claim["Origins"];
  document.getElementById("description-short").innerHTML = claim["Description"].substring(0,100);
  document.getElementById("more").innerHTML = claim["Description"].substring(100,);
  document.getElementById("example-claim").innerHTML = claim.Example;
  document.getElementById("originally-published-claim").innerHTML = claim["Originally Published"];
  document.getElementById("last-updated-claim").innerHTML = claim["Last Updated"];

}

function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    //   console.log(document.getElementById("#info-claim").style);
    //   document.getElementById("#info-claim").innerHTML = this.responseText;
    }
  };
  // xhttp.open("GET", "http://localhost:5050", true);
  // xhttp.send();
}
