### This repository contains the code for CVPR 2023 submition paper 
## WinDB: HMD-free and Distortion-free Panoptic Video Fixation Learning.

## Requirements.
Visual Studio 2019, Matlab2016b, python3.6.4, pytorch1.10.0, CUDA10.2, Opencv C++(VS);  
TobiiEyeTracker(TobiiGhost.1.7.0-Setup.exe, Tobii_Eye_Tracking_Core_v2.16.8.214_x86.exe)

## Main Steps.
### 1.WinDB Generation->2.Fixation Collection(Tobii)->3.Fixation Generation(ERP)

## The install of Tobii

## Detailed procedure：
### 1. WinDB Generation
  * 1 Generate the longitude(Lon) and latitude(Lat) of WinDB
  * 2 From ERP to WinDB based on LonLat of WinDB
### 2. Fixation Collection(Tobii)
  * 1 Open the start.sln with Visual Studio 2019
  * 2 Config property pages of start.sln 
  * 3 run the start.sln and the Location(x,y) will be saved in Fixation.txt
### 3. Fixation Generation(ERP)
  * 1 Convert the Location(x,y) of WinDB to ERP
  * 2 Smooth the fixation of ERP on the Sphere

## PanopticVideo-300 Dataset
  * 1 Video Clips:
  * 2 GroundTruth: 

## Proposed Framework(Baseline Model)
![Net](https://github.com/cvpr-submission/WinDB/tree/main/Figs/Net.png)  
  * 1 The Training Process
     ```run main.py Train=True```
  * 2 The Testing Process
     ```run main.py Test=True```
  * 3 The Model Weight
  * 4 Results
  * 5 Evaluation Code

## Please note that to meet the CVPR2023 blind requirements, this code hides the issue module and related personal information.
