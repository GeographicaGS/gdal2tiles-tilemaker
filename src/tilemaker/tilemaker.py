import os,sys,shutil
import helper

import time

if len(sys.argv) != 3: 
    print "Invalid parameteres <sources_folder> <target_folder> "
    sys.exit(-1)
    
src = sys.argv[1]
target = sys.argv[2]
ZOOM_START = 3
ZOOM_END = 17
SYS_REF = "EPSG:23030"
remove_tmp = True
remove_output_XML = True

GDAL_BIN_DIRECTORY = ""

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

tiffFile = os.path.join(tmp,"mosaic.vrt")
print "Creating big mosaic"
sys.stdout.flush()

cmd = "%s%s%s %s" % (GDAL_BIN_DIRECTORY, "#!/bin/bash\ngdalwarp -of VRT -dstalpha -r cubic "," ".join(srcFiles),tiffFile)
#gdalbuildvrt doq_index.vrt
cmd = "%s %s %s" % ("#!/bin/bash\ngdalbuildvrt -addalpha",tiffFile," ".join(srcFiles))
script_path = os.path.join(tmp,"gdalwarp_script")
text_file = open(script_path, "w")
text_file.write(cmd)
text_file.close()

os.system("chmod +x " + script_path )
os.system( script_path)
print "Mosaic created successfully"
sys.stdout.flush()


mosaic_time = time.time() - start_time

print "Creating tiles"
sys.stdout.flush()
cmd =  "%sgdal2tiles.py -r cubic -s %s -z %d-%d %s %s" % (GDAL_BIN_DIRECTORY,SYS_REF,ZOOM_START,ZOOM_END,tiffFile,target)
os.system(cmd)
print "Tiles created successfully"
sys.stdout.flush()


tiles_time = time.time() - mosaic_time - start_time

# borrado de temporales    
if remove_tmp:       
    shutil.rmtree(tmp)
    
if remove_output_XML:
    print "Removing XML files"
    sys.stdout.flush()
    
    for root, dir, files in os.walk(target):
        for file in files:
            fileName, fileExtension = os.path.splitext(file)
            if fileExtension ==".xml":
                os.unlink(os.path.join(root,file))
                
                
    print "XML files removed successfully"
    sys.stdout.flush()

    
elapsed_time = time.time() - start_time

elapsed_time = int(elapsed_time) 

print "Mosaic elapsed time: " + helper.timeString(int(mosaic_time))
print "Tiles elapsed time: " + helper.timeString(int(tiles_time))
print "Total elapsed time: " + helper.timeString(int(elapsed_time))
