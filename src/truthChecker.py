import os

def findDataPairs(folder, annotationSubFolder):
    dataPairs = []
    
    annotationFolder = os.path.join(folder, annotationSubFolder)
    if not os.path.isdir(annotationFolder):
        print("No annotations folder found at " + annotationFolder)
        return dataPairs
    imgs = os.listdir(folder)
    for img in imgs:
        imgPath = os.path.join(folder, img)
        if not os.path.isfile(imgPath):
            continue
        parts = img.rsplit('.', 1)
        base = parts[0]
        ext = parts[1]
        if len(base) is 0:
            # skip, hidden file
            continue
        xml = os.path.join(annotationFolder, base + ".xml")
        if not os.path.isfile(xml):
            print("No annotation xml found: " + xml + " for file " + imgPath)
            continue
        dataPairs.append({'img': imgPath, 'xml': xml})
    
    return dataPairs

def searchFolders(folders, annotationSubFolder):
    truthDirs = []
    
    for f in folders:
        f = os.path.abspath(f)
        if os.path.isdir(f):
            truthDirs.append(f)
        else:
            print("Directory " + str(f) + " not found, skipping...")
    
    print("found directories:")
    for t in truthDirs:
        print(t)
    
    dataPairs = []
    
    for t in truthDirs:
        newPairs = findDataPairs(t, annotationSubFolder)
        dataPairs = dataPairs + newPairs
    
    return dataPairs

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

class Annotation:
    def __init__(self, name, xmin, ymin, xmax, ymax):
        self.name = name
        self.boundingBox = BoundingBox(xmin, ymin, xmax, ymax)

import xml.etree.ElementTree as ET
def readAnnotations(xml):
    xml = os.path.abspath(xml)
    if not os.path.isfile(xml):
        print("given annotation path is not a file: " + xml)
        return []
    tree = ET.parse(xml)
    root = tree.getroot()
    annotations = []
    for obj in root.iter('object'):
        bb = obj.find('bndbox')
        xmin = bb.find('xmin').text
        ymin = bb.find('ymin').text
        xmax = bb.find('xmax').text
        ymax = bb.find('ymax').text
        ann = Annotation(obj.find('name').text, int(xmin), int(ymin), int(xmax), int(ymax))
        annotations.append(ann)
    return annotations
    def __str__(self):
        return "xmin: " + str(self.xmin) + ", xmax: " + str(self.xmax) + ", ymin: " + str(self.ymin) + ", ymax: " + str(self.ymax)

def labelsToData(dataPairs):
    annotations = []
    labels = set()
    for p in dataPairs:
        anns = readAnnotations(p['xml'])
        annotations.append(anns);
        for a in anns:
            labels.add(a.name)
    
    labelToData = {}
    for l in labels:
        labelToData[l] = []
    for i in range(0, len(dataPairs)):
        for a in annotations[i]:
			data = {}
			data['i'] = i
			data['img'] = dataPairs[i]['img']
			data['xml'] = dataPairs[i]['xml']
			data['annotation'] = a
			labelToData[a.name].append(data)
    return labelToData


if __name__ == "__main__":
    import numpy as np
    import cv2, sys
    
    print("The First argument should be the path to your ground truth folder.")
    print("<-/->: Use forward/backward arrows to navigate.")
    print("Escape: Hit escape to skip walking through a label.")
	print("Q: quit application immediately")
    
    # where-ever your ground truth folder is
    folders = sys.argv[1:]
    
    annotationSubFolder = "annotations"
    
    dataPairs = searchFolders(folders, annotationSubFolder) 
    
    print("Found " + str(len(dataPairs)) + " data pairs")
    bbColor = (255,0,0)
    bbWidth = 2
    labelToData = labelsToData(dataPairs)
    for label in labelToData.keys():
		i = 0
		while i < len(labelToData[label]):
			e = labelToData[label][i]
			imgPath = e['img']
			print(imgPath)
			a = e['annotation']
			pic = cv2.imread(imgPath,0)
			bb = a.boundingBox;
			#sub = pic[bb.ymin:bb.ymax, bb.xmin:bb.xmax]
			cv2.rectangle(pic,(bb.xmin,bb.ymin),(bb.xmax,bb.ymax),bbColor,bbWidth)
			ident = label + ": ..." + str(imgPath[-50:])
			height, width = pic.shape
			cv2.putText(pic, ident, (0,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200, 0, 0))
			cv2.imshow("img", pic)
			key = cv2.waitKey(0)
			if key == 27:
				break;
			elif key == 4:
				return
			elif key == 2: # back arrow
				i = max(i - 1, 0)
			elif key == 3: # forward arrow
				i = i + 1
			else:
				i = i + 1
  
    
