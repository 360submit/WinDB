# Import torch utils
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import models

# Basic imports
import os
import sys
import cv2
import glob
import copy
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from scipy import ndimage

# Import config file
import config

def normalize_img(value, vmax=None, vmin=None):
    #  pdb.set_trace()
    value1 = value.view(value.size(0), -1)
    value1 -= value1.min(1, keepdim=True)[0]
    value1 /= value1.max(1, keepdim=True)[0]
    return value1.view(value.size(0), value.size(1), value.size(2), value.size(3))

def MatrixNormalization(M):
    maxValue = np.max(M)
    minValue = np.min(M)
    if maxValue - minValue != 0:
        re = (M - minValue) / (maxValue - minValue)
        return re
    else:
        return M

# Test the model on an single image or on multiple images
def test_model(model, model_b, device, saliency_test_loader, multitest=False):
	
	# Test on a single image
	if not multitest:
		# Get sample (only 1)
		inputs, labels = next(iter(saliency_test_loader))
		
		# Prepare data
		inputs = inputs.to(device)

		# Predict
		model.eval()	
		pred = model(inputs)
		
		# Squeeze extra dims
		pred = np.squeeze(np.array(pred[0].detach().cpu()))

		# Clip image
		pred = np.clip(pred, 0, 1)

		
		# Save it + Show if --plot flag
		plt.imshow(pred, cmap='gray')
		plt.axis('off')
		plt.savefig(config.test_save_path + "predicted.png", bbox_inches='tight')
		if "--plot" in sys.argv:
			plt.show()
		plt.clf()
		
		if labels is not None:
			# Save original
			plt.imshow(np.squeeze(labels[0].cpu()), cmap='gray')
			plt.axis('off')
			plt.savefig(config.test_save_path + "gt.png", bbox_inches='tight')
			if "--plot" in sys.argv:
				plt.show()
			plt.clf()
	
	# Multiple image prediction
	else:
	
		i = 0
		for inputs1,inputs2,inputs3, img, labels, pathmy in saliency_test_loader:
		
			# Prepare data
			inputs1 = inputs1.to(device)
			inputs2 = inputs2.to(device)
			inputs3 = inputs3.to(device)

			# Predict
			model.eval()	
			_,pred,_ = model(inputs1,inputs2,inputs3)

			model_b.eval()	
			predb = model_b(inputs2)
			
			# Squeeze extra dims
			pred = np.squeeze(np.array(pred[0].detach().cpu()))
			predb = np.squeeze(np.array(predb[0].detach().cpu()))
			
			# Clip
			pred = np.clip(pred, 0, 1)
			predb = np.clip(predb, 0, 1)


			# Median filter
			pred = ndimage.median_filter(pred, size=9)
			predb = ndimage.median_filter(predb, size=9)

			pred =  MatrixNormalization(MatrixNormalization((pred)*(predb))+MatrixNormalization((pred)+(predb)))

			pred = MatrixNormalization(pred)*255

			img = np.squeeze(np.array(img[0].detach().cpu()))
			img = cv2.resize(img,(360,180),cv2.INTER_AREA)
			myheatmap = cv2.applyColorMap((pred).astype(np.uint8), cv2.COLORMAP_JET)
			heatmap = img +0.5*myheatmap
			
			if not os.path.exists(os.path.join(config.test_save_path,pathmy[0].split('\\')[-2])):
				os.makedirs(os.path.join(config.test_save_path,pathmy[0].split('\\')[-2]))
			
			cv2.imwrite(os.path.join(config.test_save_path,pathmy[0].split('\\')[-2],pathmy[0].split('\\')[-1][:-4]+'.png'), pred)
			cv2.imwrite(os.path.join(config.test_save_path,pathmy[0].split('\\')[-2],pathmy[0].split('\\')[-1][:-4]+'.jpg'), heatmap)

	