#!/usr/bin/env python

'''
This script takes two TMS folder sets (source and target) and performs the following procedure:

  - if a tile is present in the source set but not in the target, it will
    be copied over to the target;

  - if a tile is present in the source set and in the target, the tile in the
    source will be composed (overlayed) the tile in the target, with the result
    substituting the target tile;

  - if a tile is present in the target but not in the source, it remains there
    unaffected.

This means that the target folder is heavily modified, so be carefull. This way a small, updating
set can patch an old, much larger one.
'''
  
import os,sys,shutil
import helper
import time

if len(sys.argv) != 3: 
    print "Invalid parameteres <set_folder_1> <set_folder_2>"
    sys.exit(-1)
    
src = sys.argv[1]
target = sys.argv[2]
supportedExtensions = [".png"]

# Check if folders 
if not os.path.isdir(src):
    print "Error: Source folder [%s] does not exist." % src
    sys.exit(-1)
    
if not os.path.isdir(target):
    print "Error: Target folder [%s] does not exist." % target
    sys.exit(-1)

answer = helper.query_yes_no("Target folder structure will be modified. Continue?")

if not answer:
    print "Exiting..."
    sys.exit()

start_time = time.time()  

# Get all source files
srcFiles = []
for root, dir, files in os.walk(src):    
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension in supportedExtensions:
            coords = root.split("/")[-2:]
            coords.append(file)
            srcFiles.append("/".join(coords))

# Get all destination files            
targetFiles = []
for root, dir, files in os.walk(target):    
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension in supportedExtensions:
            coords = root.split("/")[-2:]
            coords.append(file)
            targetFiles.append("/".join(coords))

# Iterate source tiles 
for i in srcFiles:
    if i in targetFiles:
        print "%s tile present in target, merging..." % (i)
    else:
        print "%s tile not present in target, copying..." % (i)
        




    
# ZOOM_START=3
# ZOOM_END=20
# remove_tmp = False

# #list of supported extensions
# suportedExtensions = [".sid"]

# if not os.path.isdir(src):
#     print "Error: Source folder [%s] does not exist." % src
#     sys.exit(-1)
    
# if not os.path.isdir(target):
#     print "Error: Target folder [%s] does not exist." % target
#     sys.exit(-1)

# answer = helper.query_yes_no("Destination folder will be erased. Continue?")

# if not answer:
#     print "Exiting..."
#     sys.exit()

# start_time = time.time()  
 
# # cleaning target folder
# for file in os.listdir(target):
#     file_path = os.path.join(target, file)
#     if os.path.isdir(file_path):
#         if file != "tmp" or remove_tmp:
#             shutil.rmtree(file_path)
#     else:
#         os.unlink(file_path) 
    

# # get all the sources files in a list.
# srcFiles = []
# for root, dir, files in os.walk(src):    
#     for file in files:
#         fileName, fileExtension = os.path.splitext(file)        
#         if fileExtension in suportedExtensions:
#             srcFiles.append(os.path.join(root,file))
            
    

# #call to gdals
# tmp = os.path.join(target,"tmp")   
# i = 0 
# for file in srcFiles:
#     targetTmp = os.path.join(tmp,str(i))
#     print "Processing file "+file
#     sys.stdout.flush()
#     os.system("python /usr/local/gis/gdal-1.10-1/bin/gdal2tiles.py -r cubic -s EPSG:23030 -z %d-%d %s %s" % (ZOOM_START,ZOOM_END,file,targetTmp))

#     i = i+1
    
# tiles_time = time.time() - start_time

# # borrado de temporales    
# if remove_tmp:       
#     shutil.rmtree(tmp)




# print "###"
# print "Individual tiles created successfully"    
# print "###"

# print "Starting Merging process",

# # let's create the tiles for each zoom
# for zoom in range(ZOOM_START,ZOOM_END):
#     # Building a tiles dictionary to save which files appears on each tile. This will be useful to accomplish the composite of each file of tiles.  
#     tilesDict = {}
        
#     i = 0    
#     print ".",
#     sys.stdout.flush()
#     # get the tiles for each file
#     for file in srcFiles:   
        
#         targetTmp = os.path.join(tmp,str(i),str(zoom))
        
#         for row in os.listdir(targetTmp):
#             if not tilesDict.has_key(row):
#                 # first time we found this row in this zoom level 
#                 tilesDict[row] = {}
                
#             # getting all tiles in this row
#             for tile in os.listdir(os.path.join(targetTmp,row)):
#                 tileName, tileExtension = os.path.splitext(tile)
#                 # add only file .png ignore .xml files                        
#                 if tileExtension==".png":
#                     if tilesDict[row].has_key(tile):
#                         # this tile already exists in other file
#                         tilesDict[row][tile].append(str(i))                 
#                     else:
#                         # first time we found this tile               
#                         tilesDict[row][tile] = [str(i)]
                        
#         i = i+1

#     # create the tiles folder in this zoom levels
#     targetFolder = os.path.join(target,str(zoom))
#     os.makedirs(targetFolder)
    
#     for row in  tilesDict.iterkeys():
#         # create row folder
#         rowFolder = os.path.join(targetFolder,row)        
#         os.makedirs(rowFolder)
        
#         # create the tiles of the row 
#         for tile,files in tilesDict[row].iteritems():
#             if len(files)== 1:
#                 # no need of composite , copy the image directly                
#                 src = os.path.join(tmp,files[0],str(zoom),str(row),tile)
#                 dest = os.path.join(tmp,rowFolder,tile)                
#                 shutil.copyfile(src,dest)
#             else:
#                 #composite
#                 dest = os.path.join(tmp,rowFolder,tile)                
                
#                 for i in range(0,len(files)-1):
#                     if i==0:
#                         src1 = os.path.join(tmp,files[i],str(zoom),str(row),tile)
#                     else:
#                         src1 = dest                    
                    
#                     src2 = os.path.join(tmp,files[i+1],str(zoom),str(row),tile)
#                     cmd = "composite %s %s %s " % (src1,src2,dest)  
#                     os.system(cmd)
                
     
# print "OK"

# # borrado de temporales    
# if remove_tmp:       
#     shutil.rmtree(tmp)

# composite_time = time.time() - tiles_time
# elapsed_time = time.time() - start_time

# print "Tiles elapsed time: " + helper.timeString(int(tiles_time))
# print "Composite elapsed time: " + helper.timeString(int(composite_time))
# print "Total elapsed time: " + helper.timeString(int(elapsed_time))
