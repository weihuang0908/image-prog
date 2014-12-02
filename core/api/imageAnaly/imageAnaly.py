import Image
import ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from core.service.imageFun import ImageFun
imf=ImageFun()
class ImageAnaly(object):
	# def loadImage(self,filePath,resize=True):
	# 	wide=640
	# 	im = Image.open(filePath)
	# 	if resize:
	# 		hight=int(im.size[1]*wide/im.size[0])
	# 		im=im.resize((wide,hight))
	# 		im.show()
	# 	print "filePath:"+ filePath
	# 	self.I = np.array(im, dtype=np.uint16)
	
	"""
		im is image
	"""
	def histEqual(self,filePath):
		self.I=imf.loadImage(filePath)
		wide=self.I.shape[0]
		hight=self.I.shape[1]
		yuv=imf.rgb2yuv(self.I)
		patchs=[ imf.get_patch(i,j) for i in range(wide) for j in range(hight)]
		# for i in range(imf.wide):
		# 	for j in range(imf.hight):
		# 		matrix_y=np.array(yuv[imf.get_patch(i,j)][0],dtype=np.uint8)
		# 		self.imple_hist_equal(matrix_y)
		# 		yuv[i][j][0]=matrix_y[0][0]
		yuv[:,:,0]=self.imple_hist_equal(yuv[:,:,0])
		rgb=imf.yuv2rgb(yuv)
		hist_equal_im=Image.fromarray(np.array(rgb,dtype=np.uint8))
		hist_equal_im.show()

	def imple_hist_equal(self,matrix_y):
		matrix_y=np.array(matrix_y,dtype=np.uint8)
		im_y=Image.fromarray(matrix_y)
		hist=im_y.histogram()
		cdf=np.add.accumulate(hist)
		_min=matrix_y.min()
		_max=matrix_y.max()
		cdf=map(lambda i : (_max-_min) * i / max(cdf)+_min, cdf) 
		# cdf=map(lambda i : 255 * i / max(cdf), cdf) 
		for i in range(matrix_y.shape[0]):
			for j in range(matrix_y.shape[1]):
				value=matrix_y[i][j]
				matrix_y[i][j]=cdf[value]
		return matrix_y


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