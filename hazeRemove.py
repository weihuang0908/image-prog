import Image
import numpy as np
import os
class HazeRemove:

	def __init__(self):
		self.wide=640
		self.hight=480
		self.t0=0.1
		self.w0=0.9
		self.val=50
		self.w=1
		self.h=1

	def im2matrix(self,im,resize):
		if resize:
			self.hight=int(im.size[1]*self.wide/im.size[0])
			im=im.resize((self.wide,self.hight))
		else:
			self.wide=im.size[0]
			self.hight=im.size[1]
		data=np.array(im.getdata())
		self.I=np.zeros((self.wide,self.hight,3),dtype=np.int32)
		for i in range(self.wide):
			for j in range(self.hight):
				self.I[i][j]=data[i+j*self.wide]

	def get_dark_channel(self):
		self.dark_channel=np.zeros((self.wide,self.hight))
		for i in range(0,self.wide,self.w):
			for j in range(0,self.hight,self.h):
				endx=min(i+self.w,self.wide)
				endy=min(j+self.h,self.hight)
				tmp=self.I[i:endx,j:endy,:]
				self.dark_channel[i:endx,j:endy]=min(tmp.ravel())
		self.A=self.dark_channel.max()
		return(self.A,self.dark_channel)


	#slice I
	def count_low_pixNum(self,i,j):
		count=0
		endx=min(i+self.w,self.wide)
		endy=min(j+self.h,self.hight)
		for i in range(i,endx):
			for j in range(j,endy):
				if self.dark_channel[i][j]<self.val:
					count=count+1

		print str(i)+" "+str(j)+"  "+str(count)
		return count*1.0/(self.w*self.h)


	def disentangle(self):
		self.J=np.zeros((self.wide,self.hight,3),dtype=np.int32)
		self.t=np.zeros((self.wide,self.hight),dtype=np)
		for i in range(0,self.wide,self.w):
			for j in range(0,self.hight,self.h):
				endx=min(i+self.w,self.wide)
				endy=min(j+self.h,self.hight)
				pI=self.I[i:endx,j:endy,:]
				# if self.count_low_pixNum(i,j)<0.1:
				pdark_chan=self.dark_channel[i:endx,j:endy]
				pt=1-self.w0*(pdark_chan/self.A)
				self.t[i:endx,j:endy]=pt
				ptt=np.zeros((pt.shape[0],pt.shape[1],3))
				for ii in range(pt.shape[0]):
					for jj in range(pt.shape[1]):
						ptt[ii,jj,:]= max(pt[ii][jj],self.t0) *np.ones((3))
				pI= (pI-self.A)/ptt+self.A
				self.J[i:endx,j:endy,:]=pI
			
	def matrix2im(self,matrix,typeI="RGB"):
		image=Image.new(typeI,(matrix.shape[0],matrix.shape[1]))
		pixs1=image.load()
		for i in range(self.wide):
			for j in range(self.hight):
				if typeI=="RGB":
					pixs1[i,j] =tuple(matrix[i][j].tolist())
				elif typeI=="L":
					pixs1[i,j] =matrix[i][j]
		return image

	def haze_remove(self,im,w0=0.9,t0=0.1):
		self.im2matrix(im)
		self.get_dark_channel()
		self.disentangle()
		output=self.matrix2im(self.J)
		output.show()

	# some explore
	def get_dark_channel_image(self,im,resize="True"):
		self.im2matrix(im,resize)
		self.get_dark_channel()
		matrix=np.zeros((self.wide,self.hight),dtype=np.int32)
		matrix[:,:]=self.dark_channel
		im1=self.matrix2im(matrix, typeI="L")
		im1.show()
	def get_t_image(self,im,resize="True"):
		self.im2matrix(im,resize)
		self.get_dark_channel()
		self.disentangle()
		matrix=np.zeros((self.wide,self.hight),dtype=np.int32)
		matrix[:,:]=self.t*200
		print matrix
		im1=self.matrix2im(matrix, typeI="L")
		im1.show()

currentDir="/Users/weihuang/Projects/image-prog/images/mai"
maiList=os.listdir(currentDir)
hr=HazeRemove()
for im in maiList:
	if im.endswith(".jpg"):
		filePath=os.path.join(currentDir,im)
		print filePath
		im1=Image.open(filePath)
		hr.get_t_image(im1)
		# hr.get_dark_channel_image(im1,False)
