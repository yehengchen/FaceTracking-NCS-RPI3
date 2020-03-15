# Pan/tilt face tracking with a Raspberry Pi + NCS
*This project using the NCS with openvino and ServoBlaster to drive*
multiple servos via the GPIO pins
to face tracking

<img src="https://github.com/yehengchen/FaceTracking-RPI3-NCS/blob/master/img/b4lvt-8lfrb.gif" width="50%" height="50%">

### Demo video is shown [[YouTube]](https://www.youtube.com/watch?v=n2YM4_2WDlU)  [[Bilibili]](https://www.bilibili.com/video/av51621554/)
## Installation Python Libraries:
* Python 3.5
* Picamera
* OpenVINO
* Numpy
* OpenCV

## Things needed:
* A raspberry pi 3B
* A Intel® Neural Compute Stick - (NCS1/2)
* A pan/tilt bracket - ([3D printer](https://github.com/yehengchen/FaceTracking-NCS-RPI3/tree/master/3D_printer))
* Two Servos - (SG90)
* A GPIO expansion board
* Pi Camera or USB Webcam

***

### Pan/Tilt bracket

<img src="https://github.com/yehengchen/FaceTracking-RPI3-NCS/blob/master/img/3Dprint.png" width="32%" height="32%">


*Pan-and-tilt bracket - ([3D printer](https://github.com/yehengchen/FaceTracking-NCS-RPI3/tree/master/3D_printer))*

<img src="https://github.com/yehengchen/FaceTracking-RPI3-NCS/blob/master/img/Raspberry-Pi-GPIO-Layout-Model-B-Plus-rotated-2700x900-1024x341.png" width="60%" height="60%">
    
__[GPIO 4 -> PanMotor] [GPIO 17 -> TiltMotor]__
    
The code defaults to driving 8 servos, the control signals of which should be
connected to P1 header pins as follows:

    Servo number    GPIO number   Pin in P1 header   Pan-Tilt Motor
          0               4             P1-7           Pan-Motor
          1              17             P1-11          Tilt-Motor
          2              18             P1-12
          3             21/27           P1-13
          4              22             P1-15
          5              23             P1-16
          6              24             P1-18
          7              25             P1-22

***

## Install the OpenVINO™ Toolkit for Raspbian* OS Package
<img src="https://github.com/yehengchen/FaceTracking-NCS-RPI3/blob/master/img/workflow_steps.png" width="50%" height="50%">

#### FaceDetection model (IR) [./models](https://github.com/yehengchen/FaceTracking-NCS-RPI3/tree/master/models): 
* Network - face-detection-retail-0004.bin
* Weights - face-detection-retail-0004.xml

*Face detector based on SqueezeNet light (half-channels) as a backbone with a single SSD for indoor/outdoor scenes shot by a front-facing camera.*

### METHOD 1:
* #### Run this script [./Install_openvino.sh](https://github.com/yehengchen/FaceTracking-RPI3-NCS/blob/master/Install_openvino.sh)
*This script provides all instructions on install the OpenVINO™ toolkit package for Raspbian* OS*
### METHOD 2:
* #### The following steps will be covered: __[[Guide]](https://github.com/yehengchen/NCS2-OpenVINO)__
*This guide provides step-by-step instructions on how to install the OpenVINO™ toolkit for Raspbian* OS*

### To test your OpenVINO, open a new terminal. You will see the following:
        
    [setupvars.sh] OpenVINO environment initialized
***

<img src="https://github.com/yehengchen/FaceTracking-NCS-RPI3/blob/master/img/NCS.png" width="=50%" height="50%">

## Getting Started:
### Install and start multiple servos:
    git clone git@github.com:yehengchen/FaceTracking-RPI3-NCS.git
    cd FaceTracking-RPI3-NCS/ServoBlaster/user
    sudo ./servod
    
### Multiple servos testing:
    echo 0=+10 > /dev/servoblaster
    echo 1=+10 > /dev/servoblaster

### Picamera testing:
    raspistill -o image.jpg

### Run face tracking:
    python3 pi_NCS_face_traking.py

    
## Reference:
[PiBits-ServoBlaster](https://github.com/richardghirst/PiBits/tree/master/ServoBlaster)
