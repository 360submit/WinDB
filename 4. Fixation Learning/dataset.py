import os
import cv2
import random
import numpy as np
import pickle as pickle
import matplotlib.pyplot as plt

# Import config file
import config

# Import torch utilities
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets, models

# Generate two random datasets (train and val)
def get_random_datasets(total, train, val, ipath, opath, trans=None):
	r = range(0,total)
	to_train = random.sample(r, train)
	r = [x for x in r if (x not in to_train)]
	to_val = random.sample(r, val)
	train_dataset = SaliencyDataset(to_train, ipath, opath, trans)
	val_dataset = SaliencyDataset(to_val, ipath, opath, trans)
	return train_dataset, val_dataset

# Dataset class
class SaliencyDataset(Dataset):
	def __init__(self, num, input_path, sal_path, transform=None):
		self.input_path = input_path			# Input path
		self.sal_path = sal_path				# Salmaps path
		self.transform = transform				# Transformations to image
		
		self.inputs = []						# Path to dataset images (so they are not loaded in batch)
		self.salmaps = []						# Path to dataset salmaps (so they are not loaded in batch)
		
		file_names = os.listdir(self.input_path)
		for file_index in range(0, len(num)):
			file_name = file_names[num[file_index]]
			imgnames = os.listdir(os.path.join(self.input_path, file_name))
			for imgindex in range(20, len(imgnames)-11, 20):
				self.inputs.append(os.path.join(self.input_path, file_name, imgnames[imgindex]))
		
		if self.sal_path is not None:
			file_names = os.listdir(self.sal_path)
			for file_index in range(0, len(num)):
				file_name = file_names[num[file_index]]
				imgnames = os.listdir(os.path.join(self.sal_path, file_name))
				for imgindex in range(20, len(imgnames)-11, 20):
					self.salmaps.append(os.path.join(self.sal_path, file_name, imgnames[imgindex]))	
		
		# Crop the dataset to a pre-fixed subset
		self.inputs = self.inputs
		if self.sal_path is not None:
			self.salmaps = self.salmaps
		else:
			self.salmaps = None
						
	def __len__(self):
		return len(self.inputs)

	def __getitem__(self, idx):
		# Load i-th image
		image = cv2.imread(self.inputs[idx],cv2.IMREAD_COLOR)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = cv2.resize(image, (360,180), interpolation=cv2.INTER_AREA)
		image = image.astype(np.float32) / 255.0
		
		num1 = random.randrange(0,10,1)
		img_path1 = self.inputs[idx][:-8]+("%04d" % (int(self.inputs[idx][-8:-4])+num1))+'.jpg'
		image1 = cv2.imread(img_path1,cv2.IMREAD_COLOR)
		image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
		image1 = cv2.resize(image1, (360,180), interpolation=cv2.INTER_AREA)
		image1 = image1.astype(np.float32) / 255.0

		num2 = random.randrange(0,10,1)
		img_path2 = self.inputs[idx][:-8]+("%04d" %  (int(self.inputs[idx][-8:-4])+num2))+'.jpg'
		image2 = cv2.imread(img_path2,cv2.IMREAD_COLOR)
		image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
		image2 = cv2.resize(image2, (360,180), interpolation=cv2.INTER_AREA)
		image2 = image2.astype(np.float32) / 255.0

		if self.salmaps is not None:
			# Load the i-th salmap
			salmap = cv2.imread(self.salmaps[idx],cv2.IMREAD_GRAYSCALE)
			salmap = cv2.resize(salmap, (360,180), interpolation=cv2.INTER_AREA)
			salmap = salmap.astype(np.float32)/ 255.0

			salmap1 = cv2.imread(self.salmaps[idx][:-8]+("%04d" %  (int(self.salmaps[idx][-8:-4])+num1))+'.png',cv2.IMREAD_GRAYSCALE)
			salmap1 = cv2.resize(salmap1, (360,180), interpolation=cv2.INTER_AREA)
			salmap1 = salmap1.astype(np.float32)/ 255.0

			salmap2 = cv2.imread(self.salmaps[idx][:-8]+("%04d" %  (int(self.salmaps[idx][-8:-4])+num2))+'.png',cv2.IMREAD_GRAYSCALE)
			salmap2 = cv2.resize(salmap2, (360,180), interpolation=cv2.INTER_AREA)
			salmap2 = salmap2.astype(np.float32)/ 255.0
		else:
			# If salmap is not defined, return image but do not use it
			salmap = image
			
		# Apply any other transforms to image
		if self.transform:
			image = self.transform(image)
			image1 = self.transform(image1)
			image2 = self.transform(image2)
			if self.salmaps is not None:
				salmap = self.transform(salmap)
				salmap1 = self.transform(salmap1)
				salmap2 = self.transform(salmap2)

		# Return item
		if salmap is not None:
			return [image, salmap,image1, salmap1,image2, salmap2]


class SaliencyDataset1(Dataset):
	def __init__(self, num, input_path, sal_path, transform=None):
		self.input_path = input_path			# Input path
		self.sal_path = sal_path				# Salmaps path
		self.transform = transform				# Transformations to image
		
		self.inputs = []						# Path to dataset images (so they are not loaded in batch)
		self.salmaps = []						# Path to dataset salmaps (so they are not loaded in batch)
		
		file_names = os.listdir(self.input_path)
		for file_index in range(0, len(num)):
			file_name = file_names[num[file_index]]
			imgnames = os.listdir(os.path.join(self.input_path, file_name))
			for imgindex in range(1, len(imgnames)-1):
				self.inputs.append(os.path.join(self.input_path, file_name, imgnames[imgindex]))
		
		if self.sal_path is not None:
			file_names = os.listdir(self.sal_path)
			for file_index in range(0, len(num)):
				file_name = file_names[num[file_index]]
				imgnames = os.listdir(os.path.join(self.sal_path, file_name))
				for imgindex in range(1, len(imgnames)-1):
					self.salmaps.append(os.path.join(self.sal_path, file_name, imgnames[imgindex]))	
		
		# Crop the dataset to a pre-fixed subset
		self.inputs = self.inputs
		if self.sal_path is not None:
			self.salmaps = self.salmaps
		else:
			self.salmaps = None
						
	def __len__(self):
		return len(self.inputs)

	def __getitem__(self, idx):
		
		# Load i-th image
		## random -   15
		imgpaths = self.inputs[idx].split('\\')
		img_path = os.path.join(imgpaths[0]+'\\',imgpaths[-5],imgpaths[-4],imgpaths[-3])
		img_names = imgpaths[-1][-8:-4]
		imgname_1 = imgpaths[-2]+"_%04d" % (int(img_names)-1)+'.jpg'
		imgname_2 = imgpaths[-2]+"_%04d" % (int(img_names))+'.jpg'
		imgname_3 = imgpaths[-2]+"_%04d" % (int(img_names)+1)+'.jpg'

		imageori1 = cv2.imread(os.path.join(img_path, imgpaths[-2], imgname_1),cv2.IMREAD_COLOR)
		image1 = imageori1
		image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
		image1 = cv2.resize(image1, (360,180), interpolation=cv2.INTER_AREA)
		image1 = image1.astype(np.float32) / 255.0

		imageori2 = cv2.imread(os.path.join(img_path, imgpaths[-2],imgname_2),cv2.IMREAD_COLOR)
		image2 = imageori2
		image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
		image2 = cv2.resize(image2, (360,180), interpolation=cv2.INTER_AREA)
		image2 = image2.astype(np.float32) / 255.0

		imageori3 = cv2.imread(os.path.join(img_path, imgpaths[-2], imgname_3),cv2.IMREAD_COLOR)
		image3 = imageori3
		image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2RGB)
		image3 = cv2.resize(image3, (360,180), interpolation=cv2.INTER_AREA)
		image3 = image3.astype(np.float32) / 255.0

		if self.salmaps is not None:
			# Load the i-th salmap
			salmap = cv2.imread(self.salmaps[idx],cv2.IMREAD_GRAYSCALE)
			salmap = cv2.resize(salmap, (360,180), interpolation=cv2.INTER_AREA)
			salmap = salmap.astype(np.float32)/ 255.0
		else:
			# If salmap is not defined, return image but do not use it
			salmap1 = image1
			salmap2 = image2
			salmap3 = image3
			
		# Apply any other transforms to image
		if self.transform:
			image1 = self.transform(image1)
			image2 = self.transform(image2)
			image3 = self.transform(image3)
			if self.salmaps is not None:
				salmap1 = self.transform(salmap1)
				salmap2 = self.transform(salmap2)
				salmap3 = self.transform(salmap3)

		# Return item
		if salmap1 is not None:
			return [image1, image2, image3, imageori1, salmap1, self.inputs[idx]]
