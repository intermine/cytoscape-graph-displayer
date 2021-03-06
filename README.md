# cytoscape-graph-displayer
This application accepts cytoscape.js json markup and displays graphs. Designed to help visualise files generated by @nupurgunwant

Demo at http://www.intermine.org/cytoscape-graph-displayer

## Python version
Python 3.2  and all the higher versions suggested

## Dependencies
No dependency needed

## Getting started

1. After cloning/downloading, open the directory
2. Open the graph_scripts folder
3. Run the python file according to your need

To make a graph to check the number of interMines(provided by user) each class covers:
```
  import many_intm
  many_intm.find_classes("flymine", "humanmine","mousemine","ratmine")
  <add other interMines according to your need>
```
To make a graph to check if the classes of the given interMine are present in a given template or not:
```
  import one_intm_one_temp
  one_intm_one_temp.check_classes('flymine','Gene_RegionLocation')
  <add other interMine/template according to your need>
```
To make a graph to check the number of templates(provided by user) each class covers in a given interMine:
```
  import one_intm_many_temp as o
  o.check_classes('flymine','Gene_RegionLocation','GOterm_GenesInsertions','AlleleClass_Allele')
  <add other interMine/templates according to your need>
```
To make a graph to check the number of data items in each class for a given interMine:
```
  import one_intm_data as o
  o.find_classes('flymine')
  <add other interMine according to your need>
```

## Tech notes
All js/html/css assets in this folder can be served on a static server, such as apache or gh-pages. Cytoscape and jQuery are loaded via CDN, so no installation is required.  

Entry points for a developer are the index.html file and script.js for interactive functionality.  
