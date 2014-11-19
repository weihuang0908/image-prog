import Image
import numpy as np
import os

class HazeRemove(object):

	def __init__(self):
		self.wide=640
		self.hight=480
		self.t0=0.1
		self.w0=0.9
		self.val=50
		self.w=3
		self.h=3

	def loadIm(self,filePath,resize=True):
		im = Image.open(filePath)
		print resize
		if resize:
			self.hight=int(im.size[1]*self.wide/im.size[0])
			im=im.resize((self.wide,self.hight))
		else:
			self.wide=im.size[0]
			self.hight=im.size[1]
		print "filePath:"+ filePath
		self.I = np.array(im, dtype=np.int16)
		print self.I.shape
		(self.dir,self.file)=os.path.split(filePath)

	def get_patch(self,i,j):
		endx=min(i+self.w,self.wide)
		endy=min(j+self.h,self.hight)
		return np.ix_(range(j,endy),range(i,endx))

	def get_patch1(self,i,j,w,h):
		endx=min(i+w,self.wide)
		endy=min(j+h,self.hight)
		return np.ix_(range(j,endy),range(i,endx))

	def get_dark_channel(self):
		self.get_A()
		print self.A
		self.dark_channel=np.zeros((self.I.shape[0],self.I.shape[1]),np.float16)
		temp=self.I*1.0/self.A
		patchs=[ self.get_patch(i,j) for i in range(self.wide) for j in range(self.hight)]
		for i in range(self.wide):
			for j in range(self.hight):
				value=temp[self.get_patch(i,j)].min()
				self.dark_channel[j][i]=value
		print self.dark_channel[0:5][0:5]
		return(self.A,self.dark_channel)

	def get_A(self):
		dark_channel=self.I.min(axis=2)#min(r,g,b)
		patchs=[ self.get_patch(i,j) for i in range(0,self.wide,self.w) for j in range(0,self.hight,self.h)]
		for index in patchs:
			dark_channel[index]=dark_channel[index].min()
		bias=dark_channel.flatten()
		bias.sort()
		top10=bias[bias.shape[0]*0.9]
		a_set=self.I[dark_channel>top10]
		self.A=a_set[0]
		for i in range(a_set.shape[0]):
			if a_set[i].sum()>self.A.sum():
				self.A=a_set[i]
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
		self.J=np.zeros(self.I.shape,dtype=np.float16)
		self.t=np.zeros(self.I.shape,dtype=np.float16)
		for i in range(0,self.wide,self.w):
			for j in range(0,self.hight,self.h):
				patch=self.get_patch(i,j)
				pt=1-self.w0*self.dark_channel[patch]
				pt[pt<self.t0]=self.t0
				#reshape pt and get J and t
				size=(pt.shape[0],pt.shape[1],3)
				pt=np.repeat(pt,3,axis=1).reshape(size)
				self.J[patch]=(self.I[patch]-self.A)/pt+self.A
				self.t[patch]=(self.I[patch]-self.A)/(self.J[patch]-self.A+1)
		self.J[self.J>255]=255


			
	def matrix2im(self,matrix):
		matrix=np.array(matrix,dtype=np.uint8)
		image=Image.fromarray(matrix)
		return image

	def haze_remove(self,filePath,resize=True,w0=0.9,t0=0.1):
		self.loadIm(filePath,resize)
		self.get_dark_channel()
		self.disentangle()
		output=self.matrix2im(self.J)
		output.show()
		return output

	def get_S(self):
		self.R=self.I[:,:,0]
		self.G=self.I[:,:,1]
		self.B=self.I[:,:,2]
		min_rgb=self.I.min(axis=2)
		self.s_channel=1-3.0*min_rgb/(self.R+self.G+self.B)
		

	# some explore
	def get_s_image(self,filePath,resize=True):
		self.loadIm(filePath, resize)
		self.get_S()
		matrix=np.array(self.s_channel*200, np.uint8)
		im2=self.matrix2im(matrix)
		im2.show()
		return im2

	def get_dark_channel_image(self,filePath,resize="True"):
		self.loadIm(filePath, resize)
		self.get_dark_channel()
		matrix=np.array(self.dark_channel*200, np.uint8)
		im1=self.matrix2im(matrix)
		im1.show()
		return im1

	def get_t_image(self,filePath,resize=True):
		self.loadIm(filePath,resize)
		self.get_dark_channel()
		self.disentangle()
		matrix=np.array(self.t*200, np.uint8)
		im1=self.matrix2im(matrix)
		im1.show()
		return im1

	def get_ori_image(self,filePath,resize=True):
		self.loadIm(filePath,resize)
		self.get_dark_channel()
		self.disentangle()
		patch=self.get_patch1(60,60,30,10)
		matrix_dark=self.dark_channel[patch]
		print "-----dark_channel----"
		print matrix_dark[0,0:30]
		matrix_I=self.I[patch]
		print "-----I----"
		print matrix_I[0,0:30,:]
		# matrix_J=np.array(self.J[patch],np.uint8)
		print "------J---"
		print self.J[0,0:30,:]
		matrix_t=self.t[patch]
		print matrix_t[0,0:30,:]
		matrix_t=np.array(matrix_t*200, np.uint8)
		print matrix_t[0,0:30,:]
		print "---------"
		print self.A
		

		# im1=self.matrix2im(matrix_I)
		im2=self.matrix2im(self.J)
		# im1.show()
		im2.show()

