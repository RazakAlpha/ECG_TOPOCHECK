import arcpy
import os

#CREDIT: Razak Alpha (saint.alpha12@gmail.com, +233241865786)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "ECG TOPOLOGY TOOLBOX"

        # List of tool classes associated with this toolbox
        self.tools = [SCS,PWHT,PWLV, WCW, SCW, SCR, CFAMWOLOOP, SWMWOSL, SWMWOM, DUPLICATES]


class SCS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SCS"
        self.description = "STRUCTURE CROSS STRUCTURE"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure = arcpy.Parameter(name="structureLayer")
        paramStructure.displayName= "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        DESTINATION = parameters[1].valueAsText

        if os.path.exists(DESTINATION + '/' + 'SCS.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'SCS.shp')
            

        messages.addMessage("Executing on " + STRUCTURE);
        # Process: Select Layer By Location
        arcpy.SelectLayerByLocation_management(STRUCTURE, "CROSSED_BY_THE_OUTLINE_OF",STRUCTURE, "", "NEW_SELECTION", "NOT_INVERT")
        # Process: Feature Class to Feature Class
        results =  arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "SCS.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,LM_ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                                        First,#,Structure,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                                        First,#,Structure,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,
                                                                                                        First,#,Structure,Y,-1,-1""", "") 
        
        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class PWHT(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "PWHT"
        self.description = "POLES WITHOUT HIGH TENSION LINES CONNECTING TO IT"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramPole= arcpy.Parameter(name="poleLayer")
        paramPole.displayName="Select Pole Layer"
        paramPole.datatype = "Feature Layer"
        paramPole.direction ="Input"
        paramPole.parameterType= "Required"
        paramPole.filter.List = ["Point"]

        paramHTLine = arcpy.Parameter(name="htLayer")
        paramHTLine.displayName = "Select High Tension or Pole Cable Layer"
        paramHTLine.direction = "Input"
        paramHTLine.datatype = "Feature Layer"
        paramHTLine.parameterType = "Required"
        paramHTLine.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramPole,paramHTLine,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        POLE = parameters[0].valueAsText
        LINE = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + 'PWHT.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'PWHT.shp')
            

        messages.addMessage("Executing on " + POLE + ' AND ' +  LINE);
      
        # Process: Select Layer By Attribute
        arcpy.SelectLayerByAttribute_management(POLE, "NEW_SELECTION", "\"TYPE\" = 'HT_TUBULAR_33KVA' OR \"TYPE\" = 'HT_WOODEN_33KVA' OR \"TYPE\" = 'HT_PRECAST_33KVA' OR \"TYPE\" = 'HT_TUBULAR_11KVA' OR \"TYPE\" = 'HT_WOODEN_11KVA' OR \"TYPE\" = 'HT_PRECAST_11KVA'")
        # Process: Select Layer By Attribute
        arcpy.SelectLayerByAttribute_management(LINE, "ADD_TO_SELECTION", "\"TYPE\" = 'HT'")
        # Process: Select Layer By Location
        arcpy.SelectLayerByLocation_management(POLE, "INTERSECT", LINE, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        # Process: Feature Class to Feature Class
        results = arcpy.FeatureClassToFeatureClass_conversion(POLE, DESTINATION, "PWHT.shp", "", """TYPE \"TYPE\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Pole,TYPE,-1,-1;ID \"ID\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Pole,ID,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Pole,REMARKS,-1,-1;NO_OF_SL \"NO_OF_SL\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Pole,NO_OF_SL,-1,-1""", "")


        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class PWLV(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "PWLV"
        self.description = "POLES WITHOUT CONNECTING LOW VOLTAGE CABLES"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramPole= arcpy.Parameter(name="poleLayer")
        paramPole.displayName="Select Pole Layer"
        paramPole.datatype = "Feature Layer"
        paramPole.direction ="Input"
        paramPole.parameterType= "Required"
        paramPole.filter.List = ["Point"]

        paramMisc = arcpy.Parameter(name="miscPoleLayer")
        paramMisc.displayName = "Any Additional / Misc / Comment Poles Layer?"
        paramMisc.direction = "Input"
        paramMisc.datatype = "Feature Layer"
        paramMisc.parameterType = "Optional"
        paramMisc.filter.List = ["Point"]

        paramLVLine = arcpy.Parameter(name="lvLayer")
        paramLVLine.displayName = "Select Low voltage line or Pole Cable Layer"
        paramLVLine.direction = "Input"
        paramLVLine.datatype = "Feature Layer"
        paramLVLine.parameterType = "Required"
        paramLVLine.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramPole,paramLVLine,paramDestination,paramMisc]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        POLE = parameters[0].valueAsText
        LINE = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText
        COMMENTS = parameters[3].valueAsText

        if os.path.exists(DESTINATION + '/' + 'PWLV.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'PWLV.shp')
            

        messages.addMessage("Executing on " + POLE + ' AND ' +  LINE);

        if (COMMENTS):
            messages.addMessage("OPTIONAL NOT SET");
        else:
            COMMENTS = "not found"
        
      
        # Process: Select Layer By Attribute
        arcpy.SelectLayerByAttribute_management(POLE, "NEW_SELECTION", "\"TYPE\" = 'LV_PRECAST_CONCRETE' OR \"TYPE\" = 'LV_TUBULAR_STAINLESS_ST' OR \"TYPE\" = 'LV_WOODEN'")
        # Process: Select Layer By Attribute
        if arcpy.Exists(COMMENTS):
            arcpy.SelectLayerByAttribute_management(COMMENTS, "ADD_TO_SELECTION", "\"TYPE\" = 'NO CONNECTION'")
            # Process: Select Layer By Location
            arcpy.SelectLayerByLocation_management(POLE, "INTERSECT", COMMENTS, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        else:
            # Process: Select Layer By Attribute
            arcpy.SelectLayerByAttribute_management(POLE, "REMOVE_FROM_SELECTION", "\"ID\" = 'NO LINES' OR \"ID\" = 'NC' OR \"ID\" = 'NO CONNECTION'")
        # Process: Select Layer By Attribute
        arcpy.SelectLayerByAttribute_management(LINE, "ADD_TO_SELECTION", "\"TYPE\" = 'LV'")
        # Process: Select Layer By Location
        arcpy.SelectLayerByLocation_management(POLE, "INTERSECT", LINE, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        # Process: Feature Class to Feature Class
        results = arcpy.FeatureClassToFeatureClass_conversion(POLE, DESTINATION, "PWLV.shp", "", """TYPE \"TYPE\" true true false 100 Text 0 0 ,
                                                                                                First,#,Pole,TYPE,-1,-1;ID \"ID\" true true false 100 Text 0 0 ,
                                                                                                First,#,Pole,ID,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                                First,#,Pole,REMARKS,-1,-1;NO_OF_SL \"NO_OF_SL\" true true false 100 Text 0 0 ,
                                                                                                First,#,Pole,NO_OF_SL,-1,-1""", "")



        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class WCW(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "WCW"
        self.description = "WALL CROSSED BY THE OUTLINE OF OTHER WALLS"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramWAll= arcpy.Parameter(name="wallLayer")
        paramWAll.displayName = "Select Wall Layer"
        paramWAll.datatype = "Feature Layer"
        paramWAll.direction ="Input"
        paramWAll.parameterType= "Required"
        paramWAll.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramWAll,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        WALL = parameters[0].valueAsText
        DESTINATION = parameters[1].valueAsText

        if os.path.exists(DESTINATION + '/' + 'WCW.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'WCW.shp')
            

        messages.addMessage("Executing on " + WALL);
        
        # Process: Select Layer By Location
        arcpy.SelectLayerByLocation_management(WALL, "CROSSED_BY_THE_OUTLINE_OF", WALL, "", "NEW_SELECTION", "NOT_INVERT")
        # Process: Feature Class to Feature Class
        results = arcpy.FeatureClassToFeatureClass_conversion(WALL, DESTINATION, "WCW.shp", "", """TYPE \"TYPE\" true true false 100 Text 0 0 ,
                                                                                    First,#,Wall,TYPE,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                    First,#,Wall,REMARKS,-1,-1""", "")


        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class SCW(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SCW"
        self.description = "STRUCTURE CROSSED WALL BY OUTLINE"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure= arcpy.Parameter(name="structureLayer")
        paramStructure.displayName = "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramWAll= arcpy.Parameter(name="wallLayer")
        paramWAll.displayName = "Select Wall Layer"
        paramWAll.datatype = "Feature Layer"
        paramWAll.direction ="Input"
        paramWAll.parameterType= "Required"
        paramWAll.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramWAll,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        WALL = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + 'SCW.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'SCW.shp')
            

        messages.addMessage("Executing on SCW" + STRUCTURE + ' AND ' +  WALL);
        
        # Process: Select Layer By Location
        arcpy.SelectLayerByLocation_management(STRUCTURE, "CROSSED_BY_THE_OUTLINE_OF", WALL, "", "NEW_SELECTION", "NOT_INVERT")
        # Process: Feature Class to Feature Class
        results = arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "SCW.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,First,#,Structure,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,LM_ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                                    First,#,Structure,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                                    First,#,Structure,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,
                                                                                                    First,#,Structure,Y,-1,-1""", 
                                                                                                    "")


        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class SCR(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SCR"
        self.description = "STRUCTURE CROSSED ROUTE BY OUTLINE"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure= arcpy.Parameter(name="structureLayer")
        paramStructure.displayName = "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramRoute= arcpy.Parameter(name="routeLayer")
        paramRoute.displayName = "Select Route Layer"
        paramRoute.datatype = "Feature Layer"
        paramRoute.direction ="Input"
        paramRoute.parameterType= "Required"
        paramRoute.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramRoute,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        ROUTES = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + 'SCR.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'SCR.shp')
            

        messages.addMessage("Executing on SCR" + STRUCTURE + ' AND ' +  ROUTES);
        

        arcpy.SelectLayerByLocation_management(STRUCTURE, "CROSSED_BY_THE_OUTLINE_OF", ROUTES, "", "NEW_SELECTION", "NOT_INVERT")
        results = arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "SCR.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,LM_ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                            First,#,Structure,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                            First,#,Structure,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,
                                                                                            First,#,Structure,Y,-1,-1""", 
                                                                                            "")


        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class CFAMWOLOOP(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CFAMWOLOOP"
        self.description = "CONNECTED FROM ANOTHER METER WITHOUT A LOOP LINE"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure= arcpy.Parameter(name="structureLayer")
        paramStructure.displayName = "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramLoop= arcpy.Parameter(name="loopLayer")
        paramLoop.displayName = "Select Loop Line Layer"
        paramLoop.datatype = "Feature Layer"
        paramLoop.direction ="Input"
        paramLoop.parameterType= "Required"
        paramLoop.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramLoop,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        LINE = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + 'CFAMWOLOOP.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'CFAMWOLOOP.shp')
            

        messages.addMessage("Executing on CFAMWOLOOP" + STRUCTURE + ' AND ' +  LINE);
        

        arcpy.SelectLayerByAttribute_management(STRUCTURE, "NEW_SELECTION", "\"GROUP\" = 'SWMCFAM'")
        arcpy.SelectLayerByAttribute_management(LINE, "ADD_TO_SELECTION", "\"TYPE\" = 'LOOP'")
        arcpy.SelectLayerByLocation_management(STRUCTURE, "INTERSECT", LINE, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        results =  arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "CFAMWOLOOP.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,LM_ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                                First,#,Structure,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                                First,#,Structure,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,
                                                                                                First,#,Structure,Y,-1,-1""", 
                                                                                                "")


        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class SWMWOSL(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SWMWOSL"
        self.description = "STRUCTURE WITH METER WITHOUT A SERVICE LINE CONNECTED"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure= arcpy.Parameter(name="structureLayer")
        paramStructure.displayName = "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramMeter= arcpy.Parameter(name="meterLayer")
        paramMeter.displayName = "Select Meter Point Layer"
        paramMeter.datatype = "Feature Layer"
        paramMeter.direction ="Input"
        paramMeter.parameterType= "Required"
        paramMeter.filter.List = ["Point"]

        paramService= arcpy.Parameter(name="loopLayer")
        paramService.displayName = "Select Service Line Layer"
        paramService.datatype = "Feature Layer"
        paramService.direction ="Input"
        paramService.parameterType= "Required"
        paramService.filter.List = ["Line"]

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramMeter, paramService,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        METER = parameters[1].valueAsText
        LINE = parameters[2].valueAsText
        DESTINATION = parameters[3].valueAsText

        if os.path.exists(DESTINATION + '/' + 'SWMWOSL.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'SWMWOSL.shp')
            

        messages.addMessage("Executing on SWMWOSL" + STRUCTURE + ' , ' + METER +  ' AND ' +  LINE);
        

        arcpy.SelectLayerByAttribute_management(STRUCTURE, "NEW_SELECTION", "\"GROUP\" = 'MOVABLE'")
        arcpy.SelectLayerByLocation_management(STRUCTURE, "CONTAINS", METER, "", "SUBSET_SELECTION", "NOT_INVERT")
        arcpy.SelectLayerByAttribute_management(STRUCTURE, "ADD_TO_SELECTION", "\"GROUP\" = 'SWM'")
        arcpy.SelectLayerByAttribute_management(LINE, "ADD_TO_SELECTION", "\"TYPE\" = 'SL'")
        arcpy.SelectLayerByLocation_management(STRUCTURE, "INTERSECT", LINE, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        results = arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "SWMWOSL.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,LM ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                            First,#,STRUCTURE,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,
                                                                                            First,#,STRUCTURE,Y,-1,-1""", "")




        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return

class SWMWOM(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SWMWOM"
        self.description = "STRUCTURE WITH METER WITHOUT A METER CONNECTED"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramStructure= arcpy.Parameter(name="structureLayer")
        paramStructure.displayName = "Select Structure Layer"
        paramStructure.datatype = "Feature Layer"
        paramStructure.direction ="Input"
        paramStructure.parameterType= "Required"
        paramStructure.filter.List = ["Polygon"]

        paramMeter= arcpy.Parameter(name="meterLayer")
        paramMeter.displayName = "Select Meter Point Layer"
        paramMeter.datatype = "Feature Layer"
        paramMeter.direction ="Input"
        paramMeter.parameterType= "Required"
        paramMeter.filter.List = ["Point"]



        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramStructure,paramMeter,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        STRUCTURE = parameters[0].valueAsText
        METER = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + 'SWMWOM.shp'):
            arcpy.Delete_management(DESTINATION + '/' + 'SWMWOM.shp')
            

        messages.addMessage("Executing on SWMWOM" + STRUCTURE + ' , ' + METER );
        


        arcpy.SelectLayerByAttribute_management(STRUCTURE, "NEW_SELECTION", "\"GROUP\" = 'SWM'")
        arcpy.SelectLayerByLocation_management(STRUCTURE, "CONTAINS", METER, "", "REMOVE_FROM_SELECTION", "NOT_INVERT")
        results = arcpy.FeatureClassToFeatureClass_conversion(STRUCTURE, DESTINATION, "SWMWOM.shp", "", """NEW_STR_ID \"NEW_STR_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,NEW_STR_ID,-1,-1;GROUP \"GROUP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,GROUP,-1,-1;STOREY \"STOREY\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,STOREY,-1,-1;DIVISION \"DIVISION\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,DIVISION,-1,-1;LM_ID \"LM_ID\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,LM ID,-1,-1;ACT_CODE \"ACT_CODE\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,ACT_CODE,-1,-1;TIME \"TIME\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,TIME,-1,-1;REMARKS \"REMARKS\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,REMARKS,-1,-1;PDOP \"PDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,PDOP,-1,-1;HDOP \"HDOP\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,HDOP,-1,-1;RMS \"RMS\" true true false 100 Text 0 0 ,
                                                                                            First,#,STRUCTURE,RMS,-1,-1;X \"X\" true true false 19 Double 0 0 ,
                                                                                            First,#,STRUCTURE,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,F
                                                                                            irst,#,STRUCTURE,Y,-1,-1""", 
                                                                                            "")



        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return


class DUPLICATES(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DUPLICATE CHECK"
        self.description = "CHECK FOR DUPLICATE OBJECTS BASED ON A FIELD"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paramLayer= arcpy.Parameter(name="featureLayer")
        paramLayer.displayName = "Select Feature Layer"
        paramLayer.datatype = "Feature Layer"
        paramLayer.direction ="Input"
        paramLayer.parameterType= "Required"
        paramLayer.filter.list = ["Point"]


        paramField= arcpy.Parameter(name="featureField")
        paramField.displayName = "Select Duplicate Field"
        paramField.datatype = "Field"
        paramField.direction ="Input"
        paramField.parameterType= "Required"
        paramField.parameterDependencies = [paramLayer.name]
        

        paramDestination = arcpy.Parameter(name="destination")
        paramDestination.displayName = "Select Output directory"
        paramDestination.direction = "Input"
        paramDestination.datatype = "Folder"
        paramDestination.parameterType = "Required"

        return [paramLayer,paramField,paramDestination]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
       
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        LAYER =  parameters[0].valueAsText
        FIELD = parameters[1].valueAsText
        DESTINATION = parameters[2].valueAsText

        if os.path.exists(DESTINATION + '/' + FIELD + "_DUPS.shp"):
            arcpy.Delete_management(DESTINATION + '/' + FIELD + "_DUPS.shp")
            

        messages.addMessage("Executing DUPLICATE CHECKS ON " + FIELD);

        valueList = []
        cursor = arcpy.da.SearchCursor(LAYER, [FIELD])
        
        # LIST ALL VALUES FROM THE DUPLICATE FIELD
        for row in cursor:
            valueList.append(row[0])
        
        # GET ONLY THE DUPLICATED VALUES OR DISTINCT VALUES
        duplist=[]
        for item in valueList:
            if valueList.count(item)>1 and item not in duplist:
                duplist.append(item)


        # BUILD A DYNAMIC FILTER QUERY USING THE VALUES IN THE DUPLICATE LIST
        q=""
        query=""
        valueList.sort()

        for x in duplist:
            query= FIELD + "='"+str(x)+"' OR " + q
            q=query


        # TRUNCATE THE END OF THE QUERY TO REMOVE THE TRAILING ' OR '
        q=q[0:-4]

        arcpy.management.SelectLayerByAttribute(LAYER,"NEW_SELECTION",q)
        # MAKE A LAYER OUT OF THE SELECTION, NO FIELD MAPPING USED
        results = arcpy.FeatureClassToFeatureClass_conversion(LAYER, DESTINATION, FIELD + '_DUPS.shp')

        valueList=[]
        duplist =[]
        q=""
        query=""
        del cursor
        del row

        # PROGRESS REPORTS
        messages.addMessage("Feature created At " + str(results));
        messages.addMessage("Feature Directory " + os.path.dirname( str(results)));
        messages.addMessage("Feature BaseName " + os.path.basename( str(results)));

        # GET THE CURRENT MAP DOCUMENT AND BASE DATA FRAME
        MXD = arcpy.mapping.MapDocument("CURRENT")
        DF = arcpy.mapping.ListDataFrames(MXD)[0]

        # CREATE A LAYER FROM A FEATURE FILE
        layer = arcpy.mapping.Layer(os.path.dirname( str(results) + "/" +  os.path.basename( str(results))))
        # ADD CREATED LAYER TO ACTIVE MAP DATA FRAME AT TOP POSITION
        arcpy.mapping.AddLayer(DF, layer, "TOP")

        #show number of Features created
        featureCount = arcpy.GetCount_management(layer)
        messages.addMessage('{} has {} records'.format(layer, featureCount[0]))

        # MXD.save()
        del MXD

        return
