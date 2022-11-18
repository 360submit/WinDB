from torchvision import transforms
 
# Transforations to input images
trans = transforms.Compose([
	transforms.ToTensor()
])

# Total of training images
total = 240

# Number of images for training
train = 200

# Number of images for validating
# val = 80
val = 40

# Batch size for training
batch_size = 4

# Number of epochs to train
epochs = 1600

# Path to input images
ipath = "C:\\CVPR2023\\MyResizeForTrain\\frames\\"

# Path to output images
opath = "C:\\CVPR2023\\MyResizeForTrain\\maps\\"

# Path to save model
model_path = "C:\\CVPR2023\\Panoramic-CNN-360-Saliency-master加了selfatt\\models\\model.pth"
model_path_b = "C:\\CVPR2023New\\models\\model目前论文结果的RGB初始化(380,190).pth"

# Path to save checkpoints
ckpt_path = "checkpoints/model_name.tar"

# Test parameters

# Number of test images (in case you want to test multiple images)
test_total = 22

# Path to test inputs
test_ipath = "C:\\CVPR2023\\MyResizeForTest\\frames\\"

# Path to test GT outputs (to compare)
# Set it as None if there is no GT
test_opath = None

# Path to save test results
test_save_path = "C:\\CVPR2023\\Panoramic-CNN-360-Saliency-master\\result\\"
