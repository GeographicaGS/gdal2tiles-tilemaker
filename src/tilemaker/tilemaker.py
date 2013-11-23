import os,sys,shutil
import helper

import time

if len(sys.argv) != 3: 
    print "Invalid parameteres <sources_folder> <target_folder> "
    sys.exit(-1)
    
src = sys.argv[1]
target = sys.argv[2]
ZOOM_START = 3
ZOOM_END = 20
SYS_REF = "EPSG:23030"
remove_tmp = False

GDAL_BIN_DIRECTORY = "/usr/local/gis/gdal-1.10-1/bin/"

#list of supported extensions
suportedExtensions = [".sid"]

if not os.path.isdir(src):
    print "Error: Source folder [%s] does not exist." % src
    sys.exit(-1)
    
if not os.path.isdir(target):
    print "Error: Target folder [%s] does not exist." % target
    sys.exit(-1)

answer = helper.query_yes_no("Destination folder will be erased. Continue?")

if not answer:
    print "Exiting..."
    sys.exit()

start_time = time.time()  
 
# cleaning target folder
for file in os.listdir(target):
    file_path = os.path.join(target, file)
    if os.path.isdir(file_path):
        if file != "tmp" or remove_tmp:
            shutil.rmtree(file_path)        
    else:
        os.unlink(file_path) 
    

# get all the sources files in a list.
srcFiles = []
for root, dir, files in os.walk(src):    
    for file in files:
        fileName, fileExtension = os.path.splitext(file)        
        if fileExtension in suportedExtensions:
            srcFiles.append(os.path.join(root,file))
            
    


#call to gdals
tmp = os.path.join(target,"tmp")
os.makedirs(tmp)

tiffFile = os.path.join(tmp,"mosaic.tiff")
print "Creating big mosaic"
cmd = "%s%s%s %s" % (GDAL_BIN_DIRECTORY, "gdalwarp -of GTiff -dstalpha -r cubic "," ".join(srcFiles),tiffFile)
#os.system(cmd)
print "Mosaic created successfully"

mosaic_time = time.time() - start_time

print "Creating tiles"
cmd =  "python %sgdal2tiles.py -r cubic -s %s -z %d-%d %s %s" % (GDAL_BIN_DIRECTORY,SYS_REF,ZOOM_START,ZOOM_END,tiffFile,target)
os.system(cmd)
print "Tiles created successfully"

tiles_time = time.time() - start_time

# borrado de temporales    
if remove_tmp:       
    shutil.rmtree(tmp)
    
elapsed_time = time.time() - start_time

elapsed_time = int(elapsed_time) 

print "Mosaic elapsed time: " + helper.timeString(int(mosaic_time))
print "Tiles elapsed time: " + helper.timeString(int(tiles_time))
print "Total elapsed time: " + helper.timeString(int(elapsed_time))


        
        
    
    