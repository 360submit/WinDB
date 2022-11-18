import os
import sys; sys.path.append("utils")
import time; start_time = time.time()
import matplotlib.pyplot as plt


# Import config file
import config

# Import torch libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Import custom dataset class
from dataset import SaliencyDataset1

# Import network model
from spherenet_model_A import SphereNet_A		# New refactored model

from spherenet import SphereConv2D

# Import training function
from train import train_model

# Import testing function
from test import test_model


def get_time():
	return ("[" + str("{:.4f}".format(time.time() - start_time)) + "]: ")

train = True
test = False


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


if __name__ == '__main__':
		
	if train == True:	

		# Instantiate model
		model = SphereNet_A()
		device = torch.device(0)	
		model = torch.nn.DataParallel(model).cuda()
		model.to(device)

	
		print(get_time() + "Model has been loaded.")
		
		# Weight initialization (in case)
		def weight_init(m):
			if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d) or isinstance(m, SphereConv2D):
				nn.init.xavier_uniform_(m.weight.data)

		if not "--restore" in sys.argv:
			model.module.down1.apply(weight_init)
			model.module.down2.apply(weight_init)
			model.module.down3.apply(weight_init)
			model.module.down4.apply(weight_init)
			model.module.center.apply(weight_init)
			model.module.up1.apply(weight_init)
			model.module.up2.apply(weight_init)
			model.module.up3.apply(weight_init)
			model.module.up4.apply(weight_init)
			model.module.end.apply(weight_init)
		else:
			print("Weights not initializd due to restoring task")
		

		param_groups = model.module.get_parameter_groups()
		
		optimizer = optim.SGD([
        {'params': param_groups[0], 'lr': 1e-4},
        {'params': param_groups[1], 'lr': 2*1e-4},
        {'params': param_groups[2], 'lr': 10*1e-5},
        {'params': param_groups[3], 'lr': 20*1e-5}],  momentum=0.9, weight_decay=1e-5)

		# Do training
			
		restore = False
		if "--restore" in sys.argv:
			print("Restoring...")
			restore = True
		
		print(get_time() + "Starting training...")
		model, to_plot = train_model(model, optimizer, device, num_epochs=config.epochs, restore=restore)
		print(get_time() + "Training has been done.")

		plt.plot(to_plot[0])
		plt.plot(to_plot[1])
		plt.ylabel('Loss')
		plt.xlabel('Epoch')
		plt.legend(['Train loss', 'Validation loss'])
		plt.savefig("sphere_loss.png")
		plt.clf()


	elif test == True:

		# Check device o run on
		device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
		print(get_time() + "Working on " + str(device))
		
		# Load the model from disk
		PATH = config.model_path
		model = torch.load(PATH)		
		print(get_time() + "Model has been loaded.")

		# Generate a dataset with new test samples
		num = list(range(60))
		saliency_test_set = SaliencyDataset1(num,config.test_ipath,config.test_opath, transform = config.trans)

		# generate the corresponding data loader
		sal_test_loader = DataLoader(saliency_test_set, batch_size=1, shuffle=False, num_workers=0)

		# Test the model
		test_model(model, device, sal_test_loader, multitest=True)

		print(get_time() + "Testing has been done.")