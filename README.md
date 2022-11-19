### This repository contains the code for CVPR 2023 submission paper   
# WinDB: HMD-free and Distortion-free Panoptic Video Fixation Learning.  

<img width="15" height="15" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/star.gif"/> It should be emphasized that our proposed WinDB uses C++ to read Tobii fixation data, so you only need to prepare a Tobii device without any additional charging software and with a simple configuration to very easily run WinDB.

## Table of Contents
- [Requirements](#requirements)
- [Tobii Installation](#tobii-installation)
- [Main Steps](#main-steps)
- [Detailed Procedure of Eye Tracking Data:](#detailed-procedure-of-eye-tracking-data)
  * [1. WinDB Generation](#1-windb-generation)
  * [2. Fixation Collection](#2-fixation-collection)
  * [3. Fixation Generation](#3-fixation-generation)
  * [4. Fixation Learning](#4-fixation-learning)
  * [5. Evaluation](#5-evaluation)
- [PanopticVideo-300 Dataset](#panopticvideo-300-dataset)


## Requirements.  
* Visual Studio 2019   
* Matlab2016b     
* python3.6.4   
* pytorch1.10.0   
* CUDA10.2    
* Opencv python and C++  
* Tobii Eye Tracking installation package (TobiiGhost.1.7.0-Setup.exe, Tobii_Eye_Tracking_Core_v2.16.8.214_x86.exe)  

## Tobii Installation
  * 1 Install Tobii_Eye_Tracking_Core_v2.16.8.214_x86.exe and TobiiGhost.1.7.0-Setup.exe (**License.pdf**<img width="300" height="15" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/License.gif"/>).  
  * 2 Start the Tobii Eye Tracking <img width="25" height="25" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/TobiiL.GIF"/> and calibration.  

## Main Steps  
### 1. WinDB Generation -> 2. Fixation Collection -> 3. Fixation Generation -> 4. Fixation Learning -> 5. Evaluation  

## Detailed Procedure of Fixation Learning Data:  

### 1. WinDB Generation  
<div align=center><img width="900" height="380" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/pip.gif"/></div>
<p align="center">The overall pipeline of our new HMD-free fixation collection approach for panoptic data. Compared to the widely-used HMDbased method, our WinDB approach is more economical, comfortable, and reasonable. </p>    

  * 1) Generate the **longitude (lon.txt)** and **latitude (lat.txt)** of WinDB;  
  ```python ERP2WinDBLonLat.py``` 
  * 2) From ERP to WinDB based on **LonLat (lon.txt, lat.txt)** of WinDB.  
  ```python ERP2WinDB.py```
  
### 2. Fixation Collection  
<div align=center><img width="400" height="120" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/Tobii.gif"/></div>
<p align="center">The existing HMD-based method compares the advantages (+) and disadvantages (-) with our WinDB approach. </p>   

  * 1) Open the ```start.sln```<img width="75" height="25" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/start.sln.gif"/> with Visual Studio 2019;  
  * 2) Config property pages of ```start.sln```<img width="75" height="25" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/start.sln.gif"/>;    
  * 3) run the ```start.spp```<img width="90" height="30" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/start.gif"/> and the **fixation location(x, y)** will be saved in PeopleID.txt.  

### 3. Fixation Generation  
  * 1) Convert the **fixation location(x, y)** of WinDB to ERP;   
     fixation location(x, y)->WinDB location(theta, phi)->ERP Location(m, n)  
     ```python Location2WinDB.py```   
  * 2) Smooth the **fixation** of ERP on the Sphere.   
     ERP Location(m, n)->Sphere Location(theta, phi)->Sphere Smooth->saliency  
     ```python SphereSmooth.py```   

### 4. Fixation Learning
<div align=center><img width="600" height="400" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/Net.gif"/></div>
<p align="center">
The motivation of the newly proposed model.   
Subfigures A and B illustrate the “fixation shifting” phenomenon — very common in our set.   
Our model has devised “a very simple yet effective” architecture, which performs spatiotemporal self-attention to alleviate the fixation shifting-induced longdistance misalignment problem. </p>     

  * 1) The **Training** Process    
     ```Python main.py --- Train=True```  
  * 2) The **Inference** Process    
     ```Python main.py --- Test=True```  
  * 3) The **Model Weight**   
     Model.pt (51.2MB)
  * 4) Results  
     Results  
### 5. Evaluation  
  * 1) The score of every **clip**  
  ```MatricsOfMyERP.m```  
  * 2) The score of the **Testing set**   
  ```MatricsOfMyALLERP.m```
    
## PanopticVideo-300 Dataset
<div align=center><img width="400" height="400" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/class.gif"/></div>
<p align="center">The semantic categories of PanopticVideo-300 dataset. All fixations in our set are collected by WinDB. </p>   

  * Video Clips (300):  
    **Training set**: 240 clips;    
    **Testing set**: 60 clips.  

### Please note that to meet the CVPR2023 blind requirements, this code hides the issue and related personal information.  

