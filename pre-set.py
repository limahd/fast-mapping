import arcpy, os


# user inputs
perimeter = 'perimetro'
utm_zone = 22



projectFolder = arcpy.Describe(perimeter).path + '\\'
trashFolder = projectFolder + 'lixo\\'
geoprocessFolder = projectFolder + 'Geoprocessamento\\'


# create standar folders
folders = ['Geoprocessamento', 'lixo']
for folder in folders:
  if os.path.isdir(os.path.join(projectFolder, folder)):
    print('The folder ' + folder + ' already exists.')

  else:
    os.mkdir(projectFolder + folder)
    print('Folder ' + folder + ' successfully created!')


# collection of functions
# checks the names of files in a folder to rename the new feature to be created
def checkshp(shpname, folder):
  shpCount = 0
  # counts the number of files in the folder that starts with the shpname text
  for file in os.listdir(folder):
    if (file[:len(shpname)] == shpname) and (file[-3:] == 'shp'):
      shpCount+=1
  # if there is none, the final file name should be equal to the input; if there is defines as the count + 1
  if shpCount == 0:
    finalFileName = shpname
  else:
    finalFileName = shpname + '_' + str(shpCount)
  return finalFileName


# turn off the add to layout
def offLayout():
  arcpy.env.addOutputsToMap= False
# turn on the add to layout
def onLayout():
  arcpy.env.addOutputsToMap= True


# creates the buffer which will be the input for the envelope tool
envBuffer = checkshp('buffer_1000m', trashFolder)
offLayout()
arcpy.Buffer_analysis(in_features=perimeter, out_feature_class= trashFolder + envBuffer + ".shp", buffer_distance_or_field="1000 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field="", method="PLANAR")
onLayout()

# creates an envelope feature around the envBuffer
envelope = checkshp('envelope', trashFolder)
arcpy.FeatureEnvelopeToPolygon_management(in_features=trashFolder + envBuffer + '.shp', out_feature_class=trashFolder + envelope + '.shp', single_envelope="SINGLEPART")
