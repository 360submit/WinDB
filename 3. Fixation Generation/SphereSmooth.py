
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import os
from mayavi import mlab 
from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem
#import torch
from scipy.spatial.distance import cdist

nrows, ncols = (960,1920)

def near( p, pntList, d0 ):
    cnt=0
    for pj in pntList:
        dist = geodistance(p, pj)
        if dist < d0:
            cnt += 1 - dist/d0
    return cnt

def euclidean_distV2(x, y, nrows, ncols):
    dist=cdist(x,y,metric='euclidean')
    R=1
    alpha = np.arccos(1-(dist/R)**2/2)
    distance = alpha * R
    d0= 9.35*np.pi/180
    distance[distance>d0]=0
    distance=1 - distance/d0
    distance[distance==1]=0
    weight = distance.sum(axis=1) 
    weight = weight.reshape(nrows, ncols)  
    return weight

def MatrixNormalization(M):
    maxValue = np.max(M)
    minValue = np.min(M)
    if maxValue - minValue != 0:
        re = (M - minValue) / (maxValue - minValue)
        return re
    else:
        return M

def geodistance(p, pj):
    R = 1
    dist=np.linalg.norm( p - pj )
    alpha = np.arccos(1-(dist/R)**2/2)
    distance = alpha * R
    return distance

def sphereDefine():

    theta = np.linspace(0, np.pi, nrows)
    phi = np.linspace(0, 2*np.pi, ncols)

    phi,theta = np.meshgrid(phi, theta)
    # sphere
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    xm = x.flatten()
    ym = y.flatten()
    zm = z.flatten()
    sphList = np.array(np.hstack((xm[:,np.newaxis], ym[:,np.newaxis], zm[:,np.newaxis])))

    return sphList

width = 1920
height = 960

filename = './ERP/'
save_path = './ERPSmooth/'

sphList = sphereDefine()

mp4name = os.listdir(filename)
mp4name.sort()

for mp4index in range(0, len(mp4name)):
        ori_name = os.listdir(filename+mp4name[mp4index]+'/')
        ori_name.sort()

        for imgindex in range(0, len(ori_name)):
            if ori_name[imgindex].endswith('.png'):
                img = cv2.imread('./ERPImg/'+mp4name[mp4index]+'/'+ori_name[imgindex][:-4]+'.jpg')
                VRF = cv2.imread(filename+mp4name[mp4index]+'/'+ori_name[imgindex])
                [row, col] = np.where(VRF[:,:,0] > 0)
                phi = ((col + 0.5) / VRF.shape[1]) * 2 * np.pi
                theta = ((row + 0.5) / VRF.shape[0]) * np.pi
                Xs = np.sin(theta) * np.cos(phi)
                Ys = np.sin(theta) * np.sin(phi)
                Zs = np.cos(theta)
                pointList = np.array(np.hstack((Xs[:,np.newaxis], Ys[:,np.newaxis], Zs[:,np.newaxis])))
                myheatmap = euclidean_distV2(sphList, pointList, nrows, ncols)
                myheatmap = np.rint(MatrixNormalization(myheatmap) * 255)
                myheatmap = np.array(myheatmap, np.uint8)
                if not os.path.exists(save_path+mp4name[mp4index]+'/'):
                    os.makedirs(save_path+mp4name[mp4index]+'/')
                cv2.imwrite(save_path+mp4name[mp4index]+'/'+ori_name[imgindex][:-4]+'.png', myheatmap)

                if imgindex%50==0 or imgindex%51==0:
                    myheatmap = cv2.applyColorMap(myheatmap, cv2.COLORMAP_JET)
                    heatmap = img +0.5*myheatmap
                    if not os.path.exists(save_path+mp4name[mp4index]+'/'):
                        os.makedirs(save_path+mp4name[mp4index]+'/')
                    cv2.imwrite(save_path+mp4name[mp4index]+'/'+ori_name[imgindex][:-4]+'.jpg', heatmap)