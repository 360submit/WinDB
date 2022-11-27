import cv2
import sys
import os
import shutil

id = 1

def time():
	cap = cv2.VideoCapture("C:\\Users\\MSI-PC\\Desktop\\data\\"+str(id)+".mp4")    
	# file_path是文件的绝对路径，防止路径中含有中文时报错，需要解码
	if cap.isOpened():  # 当成功打开视频时cap.isOpened()返回True,否则返回False
		# get方法参数按顺序对应下表（从0开始编号)
		rate = cap.get(5)   # 帧速率
		FrameNumber = cap.get(7)  # 视频文件的帧数
		duration = round((FrameNumber/rate),5)  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
		print(type(rate),rate)
		print(type(FrameNumber),FrameNumber)
		print(type(duration),duration)
	return duration

def fm():
	cap = cv2.VideoCapture("C:\\Users\\MSI-PC\\Desktop\\data\\"+str(id)+".mp4")    
	# file_path是文件的绝对路径，防止路径中含有中文时报错，需要解码
	if cap.isOpened():  # 当成功打开视频时cap.isOpened()返回True,否则返回False
		# get方法参数按顺序对应下表（从0开始编号)
		FrameNumber = cap.get(7)  # 视频文件的帧数
	return FrameNumber

dir_pathhh = "C:\\Users\\MSI-PC\\Desktop\\data\\"+str(id)+"\\"
isExists = os.path.exists(dir_pathhh)
if not isExists:
	os.mkdir(dir_pathhh)
else:
	shutil.rmtree(dir_pathhh)
	os.mkdir(dir_pathhh)

dir_path = "C:\\Users\\MSI-PC\\Desktop\\data\\image\\"
isExists = os.path.exists(dir_path)
if not isExists:
	os.mkdir(dir_path)
else:
	shutil.rmtree(dir_path)
	os.mkdir(dir_path)

mp4 = cv2.VideoCapture("C:\\Users\\MSI-PC\\Desktop\\data\\"+str(id)+".mp4")  # 读取视频
is_opened = mp4.isOpened()  # 判断是否打开
print(is_opened)

fps = mp4.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
print(fps)
widght = mp4.get(cv2.CAP_PROP_FRAME_WIDTH)  # 获取视频的宽度
height = mp4.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 获取视频的高度
print("宽+高: ",str(widght) + "x" + str(height))


# 保存帧率与帧数
txt_path = "C:\\Users\\MSI-PC\\Desktop\\data\\"
FrameNumber = int(mp4.get(7))  # 视频文件的帧数
print("总帧数: ",FrameNumber)
full_path = txt_path+str(FrameNumber)+'_'+str(int(round(fps,0)))+'.txt'
f = open(full_path, 'a+')
f.close()

# 分帧
i = 0
while is_opened:
    if i == FrameNumber:  # 截取前FrameNumber张图片
        break
    else:
        i += 1
    (flag, frame) = mp4.read()  # 读取图片
    file_name = dir_path + str(i) + ".jpg"
    #print(file_name)
    if flag == True:
        cv2.imwrite(file_name, frame, [cv2.IMWRITE_JPEG_QUALITY])  # 保存图片
print("转换完成")
