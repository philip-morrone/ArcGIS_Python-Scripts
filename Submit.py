import arcpy

#Open file
rhinoText = open(r"C:\Users\Phil\Desktop\RhinoObservationsCSV.txt", "r")

#Read header line
headerLine = rhinoText.readline()
segmentedHeaderLine = headerLine.split(",")

#Get field indicies
observerIndex = segmentedHeaderLine.index("Observer")
xIndex = segmentedHeaderLine.index("X")
yIndex = segmentedHeaderLine.index("Y")
rhinoIndex = segmentedHeaderLine.index("Rhino")
commentIndex = segmentedHeaderLine.index("Comments\n")

#Create blank Rhino dictionary
rhinoDictionary = {}

#Create Rhino Sightings Polyline feature class
out_path = r"C:\\Users\\Phil\\Desktop\\CreateO\\"
out_name = r"RHINOTracks57.shp"
geometry_type = "POLYLINE"
spatial_reference = arcpy.SpatialReference(r"C:\Users\Phil\Desktop\Final\Data\WGS 1984.prj")
arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, "", "", "", spatial_reference)

#Add Name Field
rhinoSHP = out_path+out_name
field_name = "RHINO_NAME"
field_type = "TEXT"
arcpy.management.AddField(rhinoSHP,field_name,field_type)

#Add Comment Field
field_name1 = "COMMENT"
field_type1 = "TEXT"
arcpy.management.AddField(rhinoSHP,field_name1,field_type1)

print rhinoSHP

#Polyline function
def addPoly(cursor, array, sr, name):
    polyline = arcpy.Polyline(array, sr)
    cursor.insertRow((polyline, name))

        
#Begin looping through each line
try:
    for line in rhinoText.readlines():
        line = line.rstrip("\n")
        segmentedLine = line.split(",")

        #Determine Rhino, X, and Y referenced in line
        currentRhino = segmentedLine[rhinoIndex]
        currentX = segmentedLine[xIndex]
        currentY = segmentedLine[yIndex]
        currentComment= segmentedLine[commentIndex]

        #Create an Object of class point for the x and y coordinates
        coords = arcpy.Point(currentX, currentY)


        #If Rhino not in dictionary
        if not currentRhino in rhinoDictionary: #if Rhino is not in dictionary
            
            #Create a new object of class Array, add the point, and store Array in dictionary for particular Rhino
            coordArray = arcpy.Array() #Blank array
            coordArray.add(coords) #Add the current point to the array
            rhinoDictionary[currentRhino] = coordArray #associate the array with the current Rhino
        
                       
        #Else Rhino in dictionary
        else:
            #Get the array object from the dictionary for this Rhino and add new point to Array
            coordArray = rhinoDictionary[currentRhino] #Pull up current array of point for current Rhino
            coordArray = coordArray.add(coords) #Add additional point to array
        

    #InsertCursor begin loop
    with arcpy.da.InsertCursor(rhinoSHP, ("SHAPE@","RHINO_NAME")) as cursor:
                       
    #Print information in dictionary
        for key in rhinoDictionary:
            addPoly(cursor, rhinoDictionary[key], spatial_reference, key)
            print "Rhino Name: "+key
            print "Below are the points:"
            for p in rhinoDictionary[key]:
                print "("+str(p.X)+","+ str(p.Y)+")"
            print "==============================="
except:
    print "Epic Fail"
        
























