import os
src = "/home/sharefolder/things/tileado/00-orto56-result"
for root, dir, files in os.walk(src):
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
	if fileExtension ==".xml":
		os.unlink(os.path.join(root,file))
