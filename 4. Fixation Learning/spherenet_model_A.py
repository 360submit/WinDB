# Import torch library
import torch
import torch.nn as nn
from torch.nn import Parameter
import torch.nn.functional as F

import math

# Mesh convolutions import
from spherenet import SphereConv2D, SphereMaxPool2D

# Spherical MSE
class SphereMSE(nn.Module):
	def __init__(self, h, w):
		super(SphereMSE, self).__init__()
		pi = 3.1415926
		self.h, self.w = h, w
		weight = torch.zeros(1, 1, h, w)
		theta_range = torch.linspace(0, pi, steps=h + 1)
		dtheta = pi / h
		dphi = 2 * pi / w
		for theta_idx in range(h):
			weight[:, :, theta_idx, :] = dphi * (math.sin(theta_range[theta_idx]) + math.sin(theta_range[theta_idx+1]))/2 * dtheta
		self.weight = Parameter(weight, requires_grad=False)

	def forward(self, out, target):
		return torch.sum((out - target) ** 2 * self.weight) / out.size(0)
	
# Spherical Block = Spherical Conv + Norm + ReLU
class SphereBlock(nn.Module):
	def __init__(self, in_channels, out_channels, kernel_size=3, padding=1, dilation=1, stride=1, groups=1, is_bn=True,
				 is_relu=True):
		super(SphereBlock, self).__init__()
		# Spherical Convolution
		self.conv = SphereConv2D(in_channels, out_channels, stride=stride, bias=False)
		# Batch normalization
		self.bn = nn.BatchNorm2d(out_channels, eps=1e-4)
		# ReLU activation
		self.relu = nn.ReLU(inplace=True)
		# If no BN or ReLU indicated, then the step is avoided
		if is_bn is False: self.bn = None
		if is_relu is False: self.relu = None

	def forward(self, x):
		# Convolve input
		x = self.conv(x)
		# Batch normalize if the layer exists
		if self.bn is not None: x = self.bn(x)
		# ReLU if the layer exists
		if self.relu is not None: x = self.relu(x)
		return x

# Spherical Encoder
class SphereEncoder(nn.Module):
	def __init__(self, x_channels, y_channels, kernel_size=3):
		super(SphereEncoder, self).__init__()
		# Calculate padding
		padding = (kernel_size - 1) // 2
		# Block with two Spherical Blocks
		self.encode = nn.Sequential(
			SphereBlock(x_channels, y_channels, kernel_size=kernel_size, padding=padding, dilation=1, stride=1,
						 groups=1),
			SphereBlock(y_channels, y_channels, kernel_size=kernel_size, padding=padding, dilation=1, stride=1,
						 groups=1),
		)
		# Spherical pooling
		self.pool = SphereMaxPool2D(stride=2)

	def forward(self, x):
		# Forward input
		y = self.encode(x)
		# Pooling
		y_pooled = self.pool(y)
		# y_pooled = F.max_pool2d(y, kernel_size=2, stride=2)
		return y, y_pooled


# Mesh Decoder
class SphereDecoder(nn.Module):
	def __init__(self, x_channels, y_channels, kernel_size=3):
		super( SphereDecoder, self).__init__()
		# Calculate padding
		padding = (kernel_size - 1) // 2
		# Block with three Spherical Blocks
		self.decode = nn.Sequential(
			SphereBlock(2 * x_channels, y_channels, kernel_size=kernel_size, padding=padding, dilation=1,
						 stride=1, groups=1),	
			SphereBlock(y_channels, y_channels, kernel_size=kernel_size, padding=padding, dilation=1,
						 stride=1, groups=1),	
			SphereBlock(y_channels, y_channels, kernel_size=kernel_size, padding=padding, dilation=1,
						 stride=1, groups=1),	
		)

	def forward(self, down, x):
		N, C, H, W = down.size()
		# Upsampling
		y = F.upsample(x, size=(H, W), mode='bilinear', align_corners=True )
		y = torch.cat([y, down], 1)
		# Forward input
		y = self.decode(y)
		return y




class SphereNet_A(nn.Module):
	def __init__(self):
		super(SphereNet_A, self).__init__()

		self.down1 = SphereEncoder(3, 24, kernel_size=3)  
		self.down2 = SphereEncoder(24, 64, kernel_size=3)  
		self.down3 = SphereEncoder(64, 128, kernel_size=3)  
		self.down4 = SphereEncoder(128, 256, kernel_size=3) 

		self.center = nn.Sequential(
			SphereBlock(256, 256, kernel_size=3, padding=1, stride=1),
		)
		self.extra_gate = nn.Conv2d(256*3, 1, kernel_size  = 1, bias = False)
		self.extra_gate_s = nn.Sigmoid()
		self.extra_projf = nn.Conv2d(256*3, 256*3//2, kernel_size=1)
		self.extra_projg = nn.Conv2d(256*3, 256*3//2, kernel_size=1)
		self.extra_projh = nn.Conv2d(256*3, 256*3, kernel_size=1)
		
		self.up4 = SphereDecoder(256, 128, kernel_size=3)  
		self.up3 = SphereDecoder(128, 64, kernel_size=3)  
		self.up2 = SphereDecoder(64, 24, kernel_size=3)  
		self.up1 = SphereDecoder(24, 24, kernel_size=3)  

		self.end = SphereConv2D(24, 1, stride=1, bias=True)
		
	def forward(self, x, x1, x2):
		down1, out = self.down1(x) 
		down2, out = self.down2(out)  
		down3, out = self.down3(out)
		down4, out = self.down4(out) 
		out = self.center(out)


		down11, out1 = self.down1(x1) 
		down21, out1 = self.down2(out1)  
		down31, out1 = self.down3(out1)
		down41, out1 = self.down4(out1) 
		out1 = self.center(out1)
		
		
		down12, out2 = self.down1(x2) 
		down22, out2 = self.down2(out2)  
		down32, out2 = self.down3(out2)
		down42, out2 = self.down4(out2) 
		out2 = self.center(out2)
		
	
		outcat = self.self_attention(torch.cat((out,out1,out2), 1))

		out = outcat[:,0:256,:,:]
		out1 = outcat[:,256*1:256*2,:,:]
		out2 = outcat[:,256*2:256*3,:,:]

		out = self.up4(down4, out)
		out = self.up3(down3, out)
		out = self.up2(down2, out)
		out = self.up1(down1, out)
		out = self.end(out)
		out = torch.squeeze(out, dim=1)

		out1 = self.up4(down41, out1)
		out1 = self.up3(down31, out1)
		out1 = self.up2(down21, out1)
		out1 = self.up1(down11, out1)
		out1 = self.end(out1)
		out1 = torch.squeeze(out1, dim=1)

		out2 = self.up4(down42, out2)
		out2 = self.up3(down32, out2)
		out2 = self.up2(down22, out2)
		out2 = self.up1(down12, out2)
		out2 = self.end(out2)
		out2 = torch.squeeze(out2, dim=1)
		return out, out1, out2	

	def self_attention(self, x):
		m_batchsize, C, width, height = x.size()
		f = self.extra_projf(x).view(m_batchsize, -1, width * height) # 1,748,8,16->1,384,128
		g = self.extra_projg(x).view(m_batchsize, -1, width * height)
		h = self.extra_projh(x).view(m_batchsize, -1, width * height)

		attention     = torch.bmm(f.permute(0, 2, 1), g)
		attention     = F.softmax(attention, dim=1)

		self_attetion = torch.bmm(h, attention)
		self_attetion = self_attetion.view(m_batchsize, C, width, height)
		self_mask     = self.extra_gate(self_attetion)
		self_mask     = self.extra_gate_s(self_mask)
		out           = self_mask * x
		return out
	
	def get_parameter_groups(self):
		groups = ([], [], [], [])
		for name, value in self.named_parameters():
			if 'extra' in name:
				if 'weight' in name:
					groups[2].append(value)
				else:
					groups[3].append(value)
			else:
				if 'weight' in name:
					groups[0].append(value)
				else:
					groups[1].append(value)
		return groups