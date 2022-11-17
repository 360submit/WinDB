
import os
import cv2
import numpy as np

color1=(1, 1, 1)
color2=(0, 0, 0)

num = 0
width = 160
height = 160
u_deg = 30
v_deg = 30
wFOV = 30
hFOV = 30
rows= 6
columns = 12
mydeg = 0
equ_cx = (1920-1)/2 
equ_cy = (960-1)/2

def loadtxtmethod(filename):
    data = np.loadtxt(filename,dtype=np.float,delimiter=',')
    return data

def addRoundedRectangleBorder(): 
    cor = color2
    img = np.ones((int(160*3/2), 160*4-30*2, 3), dtype=np.uint8)
    height, width, channels = img.shape 
    border_radius = 50 
    line_thickness = 30
    edge_shift = 0
    cv2.line(img, (0, edge_shift), (width - 0, edge_shift), cor, line_thickness) 
    cv2.line(img, (0, height), (width - 0, height), cor, line_thickness) 
    cv2.line(img, (edge_shift, 0), (edge_shift, height - 0), cor, line_thickness) 
    cv2.line(img, (width, 0), (width, height - 0), cor, line_thickness) 
    #corners 
    cv2.ellipse(img, (border_radius+ edge_shift, border_radius+edge_shift), (border_radius, border_radius), 180, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, border_radius), (border_radius, border_radius), 270, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, height-border_radius), (border_radius, border_radius), 0, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (border_radius+edge_shift, height-border_radius),(border_radius, border_radius), 90, 0, 90, cor, line_thickness) 
    return img

def addRoundedRectangleBorderGray(): 
    cor = color2
    img = np.ones((int(160*3/2), 160*4, 3), dtype=np.uint8)
    height, width, channels = img.shape 
    border_radius = 40
    line_thickness = 30
    edge_shift = 0
    cv2.line(img, (0, edge_shift), (width - 0, edge_shift), cor, line_thickness) 
    cv2.line(img, (0, height), (width - 0, height), cor, line_thickness) 
    cv2.line(img, (edge_shift, 0), (edge_shift, height - 0), cor, line_thickness) 
    cv2.line(img, (width, 0), (width, height - 0), cor, line_thickness) 
    #corners 
    cv2.ellipse(img, (border_radius+ edge_shift, border_radius+edge_shift), (border_radius, border_radius), 180, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, border_radius), (border_radius, border_radius), 270, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, height-border_radius), (border_radius, border_radius), 0, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (border_radius+edge_shift, height-border_radius),(border_radius, border_radius), 90, 0, 90, cor, line_thickness) 
    return img

def addRoundedRectangleBorderGrayLine(): 
    cor = color1
    img = np.zeros((int(160*3/2), 160*4, 3), dtype=np.uint8)
    height, width, channels = img.shape 
    border_radius = 8
    line_thickness = 6
    edge_shift = 0
    cv2.line(img, (0, edge_shift), (width - 0, edge_shift), cor, line_thickness) 
    cv2.line(img, (0, height), (width - 0, height), cor, line_thickness) 
    cv2.line(img, (edge_shift, 0), (edge_shift, height - 0), cor, line_thickness) 
    cv2.line(img, (width, 0), (width, height - 0), cor, line_thickness) 
    #corners 
    cv2.ellipse(img, (border_radius+ edge_shift, border_radius+edge_shift), (border_radius, border_radius), 180, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, border_radius), (border_radius, border_radius), 270, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (width-border_radius, height-border_radius), (border_radius, border_radius), 0, 0, 90, cor, line_thickness) 
    cv2.ellipse(img, (border_radius+edge_shift, height-border_radius),(border_radius, border_radius), 90, 0, 90, cor, line_thickness) 
    return img*255

def smoothWD1(img): 
    W = int(width/2)
    M1 = img[:,0:W,:]
    M2 = img[:,W:width,:]
    kernels = [51,41,31,21,1]
    mm = 0
    resultA1 = np.empty((width,0,3),np.uint8)
    for ii in range(0, W,  int(W/5)):
        resultA1 = np.concatenate((resultA1,M1[:, ii:ii+int(W/5),:]),axis=1)
        nn = kernels[mm]
        mm = mm +1 
        resultA2 = cv2.GaussianBlur(resultA1.astype('float64'), (nn, nn), nn, 0)
        resultA1 = resultA2

    kernels = [51,41,31,21,1]
    mm = 0
    resultA3 = np.empty((width,0,3),np.uint8)
    for ii in range(W, 0, -int(W/5)):
        resultA3 = np.concatenate((M2[:, ii-int(W/5):ii,:],resultA3),axis=1)
        nn = kernels[mm]
        mm = mm +1 
        resultA4 = cv2.GaussianBlur(resultA3.astype('float64'), (nn, nn), nn, 0)
        resultA3 = resultA4
    return np.concatenate((resultA2,resultA4),axis=1)

def smoothWD2(img): 
    W = int(width/2)
    M1 = img[:,0:W,:]
    M2 = img[:,W:width,:]
    kernels = [31,21,11,1,1]
    mm = 0
    resultA1 = np.empty((width,0,3),np.uint8)
    for ii in range(0, W,  int(W/5)):
        resultA1 = np.concatenate((resultA1,M1[:, ii:ii+int(W/5),:]),axis=1)
        nn = kernels[mm]
        mm = mm +1 
        resultA2 = cv2.GaussianBlur(resultA1.astype('float64'), (nn, nn), nn, 0)
        resultA1 = resultA2

    kernels = [31,21,11,1,1]
    mm = 0
    resultA3 = np.empty((width,0,3),np.uint8)
    for ii in range(W, 0, -int(W/5)):
        resultA3 = np.concatenate((M2[:, ii-int(W/5):ii,:],resultA3),axis=1)
        nn = kernels[mm]
        mm = mm +1 
        resultA4 = cv2.GaussianBlur(resultA3.astype('float64'), (nn, nn), nn, 0) # 填充
        resultA3 = resultA4
    return np.concatenate((resultA2,resultA4),axis=1)

def addWindow():
    mask2 = np.ones((960,1920,3), dtype=np.uint8)
    cv2.line(mask2, (width*1,height*0),     (width*1,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*2,height*0),     (width*2,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*3,height*0),     (width*3,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*4,height*0),     (width*4,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*5,height*0),     (width*5,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*6,height*0),     (width*6,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*7,height*0),     (width*7,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*8,height*0),     (width*8,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*9,height*0),     (width*9,height*6),        color2, thickness=5)
    cv2.line(mask2, (width*10,height*0),    (width*10,height*6),       color2, thickness=5)
    cv2.line(mask2, (width*11,height*0),    (width*11,height*6),       color2, thickness=5)

    cv2.line(mask2, (0,height*0),           (width*columns,height*0),  color2, thickness=10)
    cv2.line(mask2, (0,height*1),           (width*columns,height*1),  color2, thickness=5)
    cv2.line(mask2, (0,height*2),           (width*columns,height*2),  color2, thickness=5)
    cv2.line(mask2, (0,height*3),           (width*columns,height*3),  color2, thickness=5)
    cv2.line(mask2, (0,height*4),           (width*columns,height*4),  color2, thickness=5)
    cv2.line(mask2, (0,height*5),           (width*columns,height*5),  color2, thickness=5)
    cv2.line(mask2, (0,height*6),           (width*columns,height*6),  color2, thickness=10)
    return mask2


def equir2pers():
    AwH = int(height*3/2)
    AwW = width*4
    #########################################################
    MaskGray = np.ones((AwH, AwW*3, 3), dtype=np.uint8)
    MaskAW = np.ones((AwH, AwW*3, 3), dtype=np.uint8)
    Back = np.ones((1080, 1920, 3), dtype=np.uint8)*255
    ######################################################

    input_vid = './Video/'
    output_dir = './Result/'
    ori_name = os.listdir(input_vid)
    ori_name.sort()

    window = addWindow()
    Borderori = addRoundedRectangleBorder()
    BorderAW = np.concatenate((np.zeros((AwH, 30, 3),np.uint8),Borderori,np.zeros((AwH, 30, 3),np.uint8)),axis=1)
    BorderGray = addRoundedRectangleBorderGray()
    for oo in range(0, 3):
        MaskGray[:,AwW*oo:AwW*(oo+1),:] = MaskGray[:,AwW*oo:AwW*(oo+1),:]*BorderGray
        MaskAW[:,AwW*oo:AwW*(oo+1),:] = MaskAW[:,AwW*oo:AwW*(oo+1),:]* BorderAW
    edgesAW = cv2.Canny(MaskAW*255, 128, 200)
    edgesAW = cv2.GaussianBlur(edgesAW,(5,5),0)
    edgesAW = cv2.merge((edgesAW,edgesAW,edgesAW))
    edgesAW[edgesAW>0]=255
    edgesGray = cv2.Canny(MaskGray*255, 128, 200)
    edgesGray = cv2.GaussianBlur(edgesGray,(1,1),0)
    edgesGray = cv2.merge((edgesGray,edgesGray,edgesGray))
    edgesGray[edgesGray>0]=255

    lon = loadtxtmethod('lon.txt') # 1440,1920
    lat = loadtxtmethod('lat.txt')
    lon = lon * equ_cx + equ_cx
    lat = lat * equ_cy + equ_cy

    for file in range(0, len(ori_name)):
        vid_name = os.path.join(input_vid, ori_name[file])

        save_path = os.path.join(output_dir, ori_name[file][:-4])
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        cap =cv2.VideoCapture(vid_name)
        num=0
        while(cap.isOpened()):
            ret, img = cap.read()
            if ret==True:                
                if len(img.shape) == 2:
                    img = img[..., None]
                ori = cv2.resize(img,(1920,960),cv2.INTER_AREA)

                persp = cv2.remap(ori, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP) 

                resultBImg = persp[0:AwH,:,:]
                resultAImg = persp[AwH:height*6+AwH,:,:]
                resultCImg = persp[height*6+AwH:height*6+AwH+AwH,:,:]

                for mm in range(0, rows):
                    for nn in range(0, columns):
                        if mm == 0 or mm == (rows-1):
                            Window = resultAImg[height*mm:height*(mm+1), width*nn:width*(nn+1),:]
                            resultAImg[height*mm:height*(mm+1), width*nn:width*(nn+1),:] = smoothWD1(Window)
                        if mm == 1 or mm == (rows-2):
                            Window = resultAImg[height*mm:height*(mm+1), width*nn:width*(nn+1),:]
                            resultAImg[height*mm:height*(mm+1), width*nn:width*(nn+1),:] = smoothWD2(Window)
                resultAImg = resultAImg*window
                for oo in range(0, 3):
                    resultBImg[:,AwW*oo:AwW*(oo+1),:] = resultBImg[:,AwW*oo:AwW*(oo+1),:]*BorderAW
                    resultCImg[:,AwW*oo:AwW*(oo+1),:] = resultCImg[:,AwW*oo:AwW*(oo+1),:]*BorderAW

                resultAImg[:AwH,:,:] = (resultAImg[:AwH,:,:]*MaskGray*0.5+resultAImg[:AwH,:,:]*(1-MaskGray))*(1-edgesGray/255)+edgesGray/1.5
                resultAImg[-AwH:,:,:] = (resultAImg[-AwH:,:,:]*MaskGray*0.5+resultAImg[-AwH:,:,:]*(1-MaskGray))*(1-edgesGray/255)+edgesGray/1.5

                Back[60:1080-60,:,:] = resultAImg
                Back[:AwH,:,:] = (resultBImg*MaskAW + Back[:AwH,:,:]*(1-MaskAW))*(1-edgesAW/255) + edgesAW/1.5
                Back[-AwH:,:,:] = (resultCImg*MaskAW + Back[-AwH:,:,:]*(1-MaskAW))*(1-edgesAW/255) + edgesAW/1.5

                cv2.imwrite(save_path+'\\'+vid_name[file][:-4]+'_%04d' % num+'.jpg', Back)
                
                print('Finished')
            num = num + 1
            print(num)
        else:
            break
        


if __name__ == '__main__':
    equir2pers()
