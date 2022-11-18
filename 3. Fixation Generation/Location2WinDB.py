import numpy as np
import cv2
from scipy import signal
import os
from PIL import Image
import os

def MaxMinNormalization(cam):
    cam = cam - np.min(cam)
    cam_img = cam / np.max(cam)
    cam_img = np.uint8(255 * cam_img)
    return cam_img

data_dir = './LocationTxt/' 
save_path = './Location2WinDB/'
ori_name = os.listdir(data_dir)
ori_name.sort()
for file in range(0, len(ori_name)):
    print(file)
    ficpath = os.path.join(data_dir, ori_name[file])
    ficname = os.listdir(ficpath)
    ficname.sort()
    txt_all = []
    for txtIndex in range(0, len(ficname)):
        vidpath = os.path.join(data_dir, ori_name[file], ficname[txtIndex])

        path = open(vidpath)
        txt_path = path.readlines()

        tmpimg = txt_path[0].strip('\n').split()[0]
        tmpimgall = []
        for ti in range(0, len(txt_path)):
            if tmpimg == txt_path[ti].strip('\n').split()[0]:
                tmpimgall.append(txt_path[ti])
            else:
                aa = tmpimgall[-1].strip('\n').split()
                bb = tmpimgall[-1].strip('\n').split()[0].split('/')[-1][:-4]
                aa.insert(0, bb)
                txt_all.append(aa)
                tmpimgall = []
                tmpimg = txt_path[ti].strip('\n').split()[0]

    pointsposi_all = []
    txt_all = sorted(txt_all)

    pointsposi = []
    nametemp = txt_all[0][0]

    for i in range(0, len(txt_all)):
        line = txt_all[i]

        if line[0] == nametemp:
            pointsposi.append(line[1:])
        else:    
            pointsposi_all.append(pointsposi)
            pointsposi = []
            pointsposi.append(line[1:])
            nametemp = line[0]
    pointsposi_all.append(pointsposi)
    pointsposi = []
    for i in range(0, len(pointsposi_all)):
        print(i)
        pointsposi = pointsposi_all[i]
        w = 960
        h = 1920
            
        img = np.zeros((w, h), dtype=np.uint8)
        img_np = np.zeros((w, h), dtype=np.uint8)

        for j in range(0, len(pointsposi)):
            line = pointsposi[j]
            if len(line)>3:
                x = int(float(line[2])-5)  # h
                y = int(float(line[3])-5) # w

            if (y<w and x<h and y>0 and x>0):
                        img_np[y][x] = 255
                        
        img = Image.fromarray(img_np)

        save_path = os.path.join(save_path, ori_name[file])

        if not os.path.exists(os.path.join(save_path, ori_name[file])):
            os.makedirs(os.path.join(save_path, ori_name[file]))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        cv2.imwrite(os.path.join(save_path, line[0].split('/')[-1][:-4]+'.png'), img_np)







