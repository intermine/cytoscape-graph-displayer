var demoFile = "http://intermine.org/cytoscape-graph-displayer/example.json",
  form = document.getElementById("myForm"),
  graph = document.getElementById("myGraph"),
  textField = document.getElementById("jsonLink"),
  cy;

//show graph when the form is submitted
myForm.addEventListener("submit", function(e) {
  e.preventDefault();

  var ourJson = e.target.jsonLink.value;
  console.log(ourJson);
  //check if it's a file or a direct copy/paste
  jsonType = fileOrJson(ourJson);
  if (jsonType == "file") {
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

function showGraph(graphElements) {
  graph.innerHTML = "";
  //tell it what element to attach to
  graphElements.container = graph;
  graphElements.layout = {
    name: "cose"
  };

  graphElements.style.push({
    "selector": "node",
    "style": {
      "background-color": "rgb(104,159,56)",
      "background-opacity": "data(weight)"
    }
  })
  //put the data inside cytoscape
  console.log("JSON loaded", graphElements);
  cy = cytoscape(graphElements);
  initExporter();
}



//show demo graph
var demo = document.getElementById("demo");
demo.addEventListener("click", function(e) {
  e.preventDefault();
  jsonLink.value = demoFile;
  document.getElementById("submitButton").click();
});


function initExporter() {
  //handle export / image download.
  //http://js.cytoscape.org/#cy.png
  var exporter = document.getElementById("export"),
  exporterFakeLink = document.getElementById("exporterFakeLink");
  exporter.addEventListener("click", function(e) {
    e.preventDefault();
    var img = cy.png();
    exporterFakeLink.setAttribute("href",img);
    exporterFakeLink.click();
  });
}
