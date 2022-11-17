
import os
import cv2
import Equirec2Perspec as E2P
import numpy as np
import copy
import datetime
from pandas import DataFrame

def equir2windblonlat():
    num = 0
    width = 160
    height = 160
    rows= 6
    columns = 12
    mydeg = 0
    ######################################################
    resultAImg = np.zeros((int(height*rows),int(width*columns), 3), dtype=np.float)
    resultAlonlat = np.zeros((int(height*rows),int(width*columns), 2), dtype=np.float)
    resultBImg = np.zeros((int(height*3/2),int(width*4)*3, 3), dtype=np.float)
    resultBlonlat = np.zeros((int(height*3/2),int(width*4)*3, 2), dtype=np.float)
    resultCImg = np.zeros((int(height*3/2),int(width*4)*3, 3), dtype=np.float)
    resultClonlat = np.zeros((int(height*3/2),int(width*4)*3, 2), dtype=np.float)
    ######################################################
    time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    print(time_now)

    ficpath = './Video/209.mp4'
    num = 0

    cap =cv2.VideoCapture(ficpath)

    while(cap.isOpened()):
        ret, img = cap.read()
        if ret==True:
            if len(img.shape) == 2:
                img = img[..., None]
            if num > 0:
                break
            num = num + 1
            for mydeg in range(0, 1):
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, 75, height, width, mydeg)
                    resultAlonlat[height*0:height*1, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*0:height*1, width*nn:width*(nn+1), :] = Perimg
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, 45, height, width, mydeg)
                    resultAlonlat[height*1:height*2, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*1:height*2, width*nn:width*(nn+1), :] = Perimg
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, 15, height, width, mydeg)
                    resultAlonlat[height*2:height*3, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*2:height*3, width*nn:width*(nn+1), :] = Perimg
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, -15, height, width, mydeg)
                    resultAlonlat[height*3:height*4, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*3:height*4, width*nn:width*(nn+1), :] = Perimg
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, -45, height, width, mydeg)
                    resultAlonlat[height*4:height*5, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*4:height*5, width*nn:width*(nn+1), :] = Perimg
                for nn in range(0, columns):
                    mu_deg = -165+nn*30
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(30, 30, mu_deg, -75, height, width, mydeg)
                    resultAlonlat[height*5:height*6, width*nn:width*(nn+1), :] = lonlat
                    resultAImg[height*5:height*6, width*nn:width*(nn+1), :] = Perimg

                for nn in range(0, 3):
                    mu_deg = -120+nn*120
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(80, 48, mu_deg, 68, int(height*3/2), width*4, mydeg)
                    resultBlonlat[0:int(height*3/2), width*4*nn:width*4*(nn+1), :] = lonlat[0:int(height*3/2),0:width*4,:]
                    resultBImg[0:int(height*3/2), width*4*nn:width*4*(nn+1), :] = Perimg[0:int(height*3/2),0:width*4,:]
                for nn in range(0, 3):
                    mu_deg = -120+nn*120
                    equ = E2P.Equirectangular(img)
                    Perimg, lonlat = equ.GetPerspective(80, 48, mu_deg, -68, int(height*3/2), width*4, mydeg)
                    resultClonlat[0:int(height*3/2), width*4*nn:width*4*(nn+1), :] = lonlat[0:int(height*3/2),0:width*4,:]
                    resultCImg[0:int(height*3/2), width*4*nn:width*4*(nn+1), :] = Perimg[0:int(height*3/2),0:width*4,:]

                resultImg = np.concatenate((resultBImg, resultAImg, resultCImg),axis=0)
                resultlonlat = np.concatenate((resultBlonlat, resultAlonlat, resultClonlat),axis=0)

                np.savetxt("./lon.txt", resultlonlat[:,:,0],fmt='%.4f',delimiter=',')
                np.savetxt("./lat.txt", resultlonlat[:,:,1],fmt='%.4f',delimiter=',')
                
                print('Finished')
            num = num + 1
            print(num)
        else:
            break
    


if __name__ == '__main__':
    equir2windblonlat()
