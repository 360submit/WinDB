import os
import sys
import cv2
import numpy as np

class Equirectangular:
    def __init__(self, img):
        self._img = img
        [self._height, self._width, _] = self._img.shape
    
    def GetPerspective(self, wFOV, hFOV, THETA, PHI, height, width, mydeg):

        equ_cx = (self._width - 1) / 2.0
        equ_cy = (self._height - 1) / 2.0

        w_len = np.tan(np.radians(wFOV / 2.0))
        h_len = np.tan(np.radians(hFOV / 2.0))
        
        x_map = np.ones([height, width], np.float32)
        y_map =  np.tile(np.linspace(-w_len, w_len, width),  [height, 1]) 
        z_map = -np.tile(np.linspace(-h_len, h_len, height), [width,  1]).T
        D = np.sqrt(x_map**2 + y_map**2 + z_map**2)                  
        xyz = np.stack((x_map, y_map, z_map), axis=2)/np.repeat(D[:, :, np.newaxis], 3, axis=2) 
        
        y_axis = np.array([0.0, 1.0, 0.0], np.float32) 
        z_axis = np.array([0.0, 0.0, 1.0], np.float32)
        [R1, _] = cv2.Rodrigues(z_axis * np.radians(THETA))
        [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-PHI))
        xyz = xyz.reshape([height * width, 3]).T
        xyz = np.dot(R1, xyz)
        xyz = np.dot(R2, xyz).T

        lon = np.arctan2(xyz[:, 1], xyz[:, 0]).reshape([height, width])
        lat = np.arcsin(xyz[:, 2]).reshape([height, width])

        lonmy = (lon / np.pi) 
        latmy = (-lat / np.pi) * 2
        lon = lonmy * equ_cx + equ_cx
        lat = latmy * equ_cy + equ_cy

        lonlatmy=np.stack((lonmy, latmy), axis=2) 
        persp = cv2.remap(self._img, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP) 

        return persp, lonlatmy
