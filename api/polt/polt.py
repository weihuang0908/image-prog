import Image
import ImageDraw
import numpy as np
import os
import matplotlib.pyplot as plt
class Polt(object):
	def showHist(self,im, w=512, h=512):
	    hist = im.histogram()
	    hist = map(lambda i : h - h * i / max(hist), hist) 
	    w = w % 256 and 256 * (w / 256 + 1) or w 
	    im2 = Image.new('L', (w, h), 255)
	    draw = ImageDraw.Draw(im2)
	    step = w / 256 
	    [draw.rectangle([i * step, hist[i], (i+1) * step, h], fill=0) for i in range(256)]
	    im2.show()
	    return im2
	def showBar(self,im,output):
		hist = im.histogram()
		plt.bar(range(0,256),hist)
		plt.savefig(output+".png")