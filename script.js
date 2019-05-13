var form = document.getElementById("myForm"),
  graph = document.getElementById("myGraph");

myForm.addEventListener("submit", function(e) {
  e.preventDefault();
  var fileToGet = e.target.jsonLink.value;
  console.log(fileToGet);
  //grab data from the file
  $.ajax(fileToGet).done(function(response){
    console.log("JSON loaded",response);
    //tell it what element to attach to
    response.container = graph;
    response.layout = {name : "cose"};
    //put the data inside cytoscape
    cytoscape(response);
  }).fail(function(response){
    //let people know if it goes wrong
    console.error(response);
    graph.innerHTML = "Error loading " + fileToGet + " " + response.status
    + " " + response.statusText;
  });
});
