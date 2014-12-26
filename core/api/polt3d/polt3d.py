import Image
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from core.service.imageFun import ImageFun
imf=ImageFun()
class Polt3d(object):
	def __init__(self):
		self.wide=640
		self.hight=480
		pass

	def loadIm(self,filePath,resize=True):
		im = Image.open(filePath)
		if resize:
			self.hight=int(im.size[1]*self.wide/im.size[0])
			im=im.resize((self.wide,self.hight))
		else:
			self.wide=im.size[0]
			self.hight=im.size[1]
		print filePath
		self.im = np.array(im, dtype=np.uint8)
		(self.dir,self.file)=os.path.split(filePath)

	def imrange(self,x,y,c,step=10,w=200,h=200):
		return self.im[x:x+w:step,y:y+h:step,c]


	def run3d(self):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		n = 100
		for c, m, x, y in [('r', 'o', 0, 0)]:
		    xs = np.ravel(self.imrange(x,y,0,10,self.wide,self.hight))
		    ys = np.ravel(self.imrange(x,y,1,10,self.wide,self.hight))
		    zs = np.ravel(self.imrange(x,y,2,10,self.wide,self.hight))
		    ax.scatter(xs, ys, zs, c=c, marker=m)
		ax.set_xlabel('R Label')
		ax.set_ylabel('G Label')
		ax.set_zlabel('B Label')
		# ax.axis(0,255,0,255)
		output=self.file.split(".")[0]+"_scatter.jpg"
		plt.savefig(output)
	def run2d(self,channel):
		fig = plt.figure()
		n = 100
		x=0
		y=0
		if channel=="b":
		    xs = np.ravel(self.imrange(x,y,0,10,self.wide,self.hight))
		    ys = np.ravel(self.imrange(x,y,1,10,self.wide,self.hight))
		elif channel=="g":
		    xs = np.ravel(self.imrange(x,y,0,10,self.wide,self.hight))
		    ys = np.ravel(self.imrange(x,y,2,10,self.wide,self.hight))
		else:
		    xs = np.ravel(self.imrange(x,y,1,10,self.wide,self.hight))
		    ys = np.ravel(self.imrange(x,y,2,10,self.wide,self.hight))
		plt.plot(xs,ys,"ro")
		# ax.axis(0,255,0,255)
		output=self.file.split(".")[0]+"_"+str(channel)+"_scatter.jpg"
		plt.savefig(output)
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

currentDir="/Users/weihuang/Projects/image-prog/images/sunny"
maiList=os.listdir(currentDir)
plot3D=Polt3d()
for i in range(1,len(maiList)):
	filePath=currentDir+"/"+maiList[i]
	plot3D.loadIm(filePath)
	plot3D.run3d()
	# plot3D.run2d("r")
	# plot3D.run2d("g")
	# plot3D.run2d("b")