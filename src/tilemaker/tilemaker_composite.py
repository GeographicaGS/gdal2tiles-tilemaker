#!/usr/bin/env python

'''
This script takes two TMS folder sets (source and target) and performs the following procedure:

  - if a tile is present in the source set but not in the target, it will
    be copied over to the target;

  - if a tile is present in the source set and in the target, the tile in the
    source will be composed (overlayed) the tile in the target, with the result
    substituting the target tile. A copy of the original target tile will be generated
    with the .orig extension attached;

  - if a tile is present in the target but not in the source, it remains there
    unaffected.

This means that the target folder is heavily modified, so be carefull. This way a small, updating
set can patch an old, much larger one.
'''
  
import os,sys,shutil
import helper
import time
from wand.image import Image
from wand.drawing import Drawing

if len(sys.argv) != 4: 
    print "Invalid parameteres <source set> <target set> <keep originals: true|false>"
    sys.exit(-1)
    
src = sys.argv[1]
target = sys.argv[2]
keepOriginals = sys.argv[3]
supportedExtensions = [".png"]

start_time = time.time()
copiedTiles = 0
mergedTiles = 0

# Check if folders 
if not os.path.isdir(src):
    print "Error: Source folder [%s] does not exist." % src
    sys.exit(-1)
    
if not os.path.isdir(target):
    print "Error: Target folder [%s] does not exist." % target
    sys.exit(-1)

answer = helper.query_yes_no("Target folder structure and files will be modified. Continue?")

if not answer:
    print "Exiting..."
    sys.exit()

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
        # Backup image
        if keepOriginals=="true":
            shutil.copy(target+"/"+i, target+"/"+i+".orig")
        else:
            pass
        # Merge images with Wand / ImageMagick
        sourceImg = Image(filename=src+"/"+i)
        targetImg = Image(filename=target+"/"+i)
        draw = Drawing()
        draw.composite(image=sourceImg, operator='src_over', left=0, top=0, width=sourceImg.width, height=sourceImg.height)
        draw.draw(targetImg)
        targetImg.save(filename=target+"/"+i)
        mergedTiles = mergedTiles+1
    else:
        # Recreate path if needed
        try:
            os.makedirs(target+"/".join(i.split("/")[:-1]))
        except:
            pass
        shutil.copy(src+"/"+i, target+"/"+i)
        copiedTiles = copiedTiles+1

elapsed_time = time.time()-start_time


print "Total copied tiles: %s" % (copiedTiles)
print "Total merged tiles: %s" % (mergedTiles)
print "Total elapsed time: %s " % (helper.timeString(int(elapsed_time)))
