import Image
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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