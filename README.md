
# ECG TOPOLOGY CHECK TOOLS 

Sets of arcpy scripts for topology and standards conformity check for arcGis toolbox. 
The toolbox features 10 tools or classes for various operations and checks including structural overlaps, duplicates, etc
## Concept
ECG TOPOOLOGY CHECK TOOLS was built mainly for the ecg assets mapping opertion in Ghana. 
However, the tools can be modified to remove the static references it make it completely dynamic tool for any datasource
## Tools in Toolbox

### SCS- STRUCTURE CROSS STRUCTURE
This tool lists all structures that crosses outline with any other structure on the same layer.
The resutls is extracted to a feature class with the destination provided as parameter


### PWHT- POLES WITHOUT HIGH TENSION LINES CONNECTING TO IT
...
### PWLV- POLES WITHOUT CONNECTING LOW VOLTAGE CABLES
...
### WCW- WALL CROSSED BY THE OUTLINE OF OTHER WALLS
...
### SCW- STRUCTURE CROSSED WALL BY OUTLINE
...
### SCR- STRUCTURE CROSSED ROUTE BY OUTLINE
...
### CFAMWOLOOP- CONNECTED FROM ANOTHER METER WITHOUT A LOOP LINE
...
### SWMWOSL- STRUCTURE WITH METER WITHOUT A SERVICE LINE CONNECTED
...
### SWMWOM- STRUCTURE WITH METER WITHOUT A METER CONNECTED
...
### DUPLICATES- CHECK FOR DUPLICATE OBJECTS BASED ON A FIELD
Scans the selected layer features for a duplicate value in attributes table. the tool allows you to select a layer, a field and destination to save all duplicates as new featureclass

## Usage/Examples
Open/ import to  Arcgis toolbox and open tools to use
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@RazakAlpah](https://github.com/RazakAlpha)

