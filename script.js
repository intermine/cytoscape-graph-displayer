var demoFile = "http://intermine.org/cytoscape-graph-displayer/example.json",
  form = document.getElementById("myForm"),
  graph = document.getElementById("myGraph"),
  textField = document.getElementById("jsonLink");

//show graph when the form is submitted
myForm.addEventListener("submit", function(e) {
  e.preventDefault();

  var ourJson = e.target.jsonLink.value;
  console.log(ourJson);
  //check if it's a file or a direct copy/paste
  jsonType = fileOrJson(ourJson);
  if(jsonType == "file") {
    loadFile(ourJson);
  } else {
    if (jsonType == "json") {
      showGraph(JSON.parse(ourJson));
    }
  }
});

function loadFile(ourJson) {
  //grab data from a remote file
  $.ajax(ourJson).done(function(response) {
    showGraph(response);
  }).fail(function(response) {
    //let people know if it goes wrong
    console.error(response);
    graph.innerHTML = "Error loading " + ourJson + " " + response.status +
      " " + response.statusText;
  });
}



function fileOrJson(aString) {
  if (aString.startsWith("http")) {
    return "file";
  } else {
    if (aString.startsWith("{")) {
      return "json";
    } else {
      console.error("neither json nor file")
      return "error";
    }
  }
}

function showGraph(graphElements){
  graph.innerHTML = "";
  console.log("JSON loaded", graphElements);
  //tell it what element to attach to
  graphElements.container = graph;
  graphElements.layout = {
    name: "cose"
  };
  //put the data inside cytoscape
  cytoscape(graphElements);
}


//show demo graph
var demo = document.getElementById("demo");
demo.addEventListener("click", function(e) {
  e.preventDefault();
  jsonLink.value = demoFile;
  document.getElementById("submitButton").click();
});
