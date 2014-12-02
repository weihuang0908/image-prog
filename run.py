import Image
import numpy as np
import os
import matplotlib.pyplot as plt
from core.api.polt import Polt
from core.api.hazeRemove import HazeRemove
from test.test import TestCase
import sys

tc=TestCase()
currentDir="/Users/weihuang/Projects/image-prog/res/images/tResearch"
outputDir="/Users/weihuang/Projects/image-prog/res/images/output/tResearch"
maiList=os.listdir(currentDir)

def test_haze_remove():
	for im in maiList:
		if im.lower().endswith(".jpg"):
			outPath=os.path.join(outputDir,im)
			f=os.path.splitext(outPath)[0]
			print f
			filePath=os.path.join(currentDir,im)
			hr=HazeRemove()
			# hr.get_s_image(filePath).save(f+"_s.jpg")
			# hr.get_dark_channel_image(filePath).save(f+"_dark_channel.jpg")
			hr.get_t_image(filePath).save(f+"_t3.jpg")
			# hr.haze_remove(filePath).save(f+"_haze_remove.jpg")

def test_polt():
	polt=Polt()
	for im in maiList:
		if im.lower().endswith(".jpg"):
			outPath=os.path.join(outputDir,im)
			f=os.path.splitext(outPath)[0]
			filePath=os.path.join(currentDir,im)
			im=Image.open(filePath)
			polt.showBar(im,f+"_bar")

def main():
	# test_polt()
	test_haze_remove()
if __name__ == '__main__':
	# main()
	tc.test()
	# hr=HazeRemove()
	# # filePath=currentDir+"/P1150672.JPG"
	# # hr.get_s_image(filePath)
	# filePath=currentDir+"/p4.JPG"
	# hr.haze_remove(filePath,resize=False)
	# hr.get_t_image(filePath)