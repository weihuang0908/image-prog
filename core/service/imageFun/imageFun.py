import Image
import numpy as np
import os



class ImageFun(object):

	def __init__(self):
		self.wide=640
		self.hight=480
		self.t0=0.1
		self.w0=0.9
		self.val=50
		self.w=3
		self.h=3
	"""
		transform specifc imamge to int16 matrix
	"""

	def loadImage(self,filePath,resize=True):
		im = Image.open(filePath)
		print resize
		if resize:
			self.hight=int(im.size[1]*self.wide/im.size[0])
			im=im.resize((self.wide,self.hight))
		print "filePath:"+ filePath
		I = np.array(im, dtype=np.int16)
		return I

	def get_patch(self,i,j):
		endx=min(i+self.w,self.wide)
		endy=min(j+self.h,self.hight)
		return np.ix_(range(j,endy),range(i,endx))

	def get_patch1(self,i,j,w,h):
		endx=min(i+w,self.wide)
		endy=min(j+h,self.hight)
		return np.ix_(range(j,endy),range(i,endx))

			
	def matrix2im(self,matrix):
		matrix=np.array(matrix,dtype=np.uint8)
		image=Image.fromarray(matrix)
		return image
	"""
		rgb is m*n*3 matrix
	"""
	def rgb2yuv(self,rgb):
		yuv=np.zeros(rgb.shape,dtype=np.float16)
		b=np.array([0,128,128])
		T=np.array([[0.299,0.587,0.114],[-0.169,-0.331,0.5],[0.5,-0.419,-0.081]])
		for i in range(rgb.shape[0]):
			for j in range(rgb.shape[1]):
				yuv[i][j]=np.dot(T,rgb[i][j].T)+b
		yuv=np.array(yuv, np.uint16)
		return yuv
	def yuv2rgb(self,yuv):
		rgb=np.zeros(yuv.shape,dtype=np.float16)
		b=np.array([0,-128,-128])
		T=np.array([[1,-0.00093,1.401687],[1,-0.3407,-0.71417],[1,1.77216,0.00099]])
		for i in range(yuv.shape[0]):
			for j in range(yuv.shape[1]):
				rgb[i][j]=np.dot(T,yuv[i][j].T+b)
				rgb[i][j][rgb[i][j]>255]=255
				rgb[i][j][rgb[i][j]<0]=0
		rgb=np.array(rgb, np.uint16)
		return rgb


