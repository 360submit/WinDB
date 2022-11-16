### This repository contains the code for CVPR 2023 submition paper   
## WinDB: HMD-free and Distortion-free Panoptic Video Fixation Learning.  

## Requirements.  
* Visual Studio 2019   
* Matlab2016b     
* python3.6.4   
* pytorch1.10.0   
* CUDA10.2    
* Opencv python and C++(VisualStudio)   
* Tobii Eye Tracking(TobiiGhost.1.7.0-Setup.exe, Tobii_Eye_Tracking_Core_v2.16.8.214_x86.exe)  

## Main Steps.  
### 1.WinDB Generation->2.Fixation Collection(Tobii)->3.Fixation Generation(ERP)  

## The Install of Tobii  
  * 1 Install Tobii_Eye_Tracking_Core_v2.16.8.214_x86.exe and TobiiGhost.1.7.0-Setup.exe (License.pdf)  
  * 2 run Tobii Eye Tracking and calibration.  

## Detailed procedure： 
### 1. WinDB Generation  
<div align=center><img width="900" height="380" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/pip.gif"/></div>
  * 1 Generate the longitude(lon.txt) and latitude(lat.txt) of WinDB  
  ```python ERP2WinDBLonLat.py``` 
  * 2 From ERP to WinDB based on LonLat of WinDB  
  ```python ERP2WinDB.py```
### 2. Fixation Collection(Tobii)  
  * 1 Open the ```start.sln``` with Visual Studio 2019  
  * 2 Config property pages of ```start.sln```    
  * 3 run the ```start.sln``` and the Fixation Location(x,y) will be saved in PeopleID.txt  
### 3. Fixation Generation(ERP)  
  * 1 Convert the Location(x,y) of WinDB to ERP  
  * 2 Smooth the fixation of ERP on the Sphere  

## PanopticVideo-300 Dataset
<div align=center><img width="400" height="400" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/class.gif"/></div>
  * 1 Video Clips (300):  
  * 2 GroundTruth (300):   

## Proposed Framework(Baseline Model)
<div align=center><img width="600" height="400" src="https://github.com/cvpr-submission/WinDB/blob/main/Figs/Net.gif"/></div>
<p align="center">
Figure 1: The motivation of the newly proposed model. Subfigures A and B illustrate the “fixation shifting” phenomenon — very common in our set. Our model has devised a very simple yet effective architecture, which performs spatiotemporal self-attention to alleviate the fixation shifting-induced longdistance misalignment problem. </p>     

  * 1 The Training Process    
     ```main.py Train=True```  
  * 2 The Testing Process    
     ```main.py Test=True```  
  * 3 The Model Weight   
     Model.pt  
  * 4 Results  
     Results  
  * 5 Evaluation Code (Matlab)  
    ```MatricsOfMyERP.m``` and ```MatricsOfMyALLERP.m```

## Please note that to meet the CVPR2023 blind requirements, this code hides the issue module and related personal information.
