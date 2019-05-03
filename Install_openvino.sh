#!/bin/bash
# openvino installer for raspberry pi. This allows you to test the Intel Neural Compute Stick v2
# based on https://software.intel.com/en-us/articles/OpenVINO-Install-RaspberryPI
# assumes Raspberry Pi Raspbian Stretch November 2019
# have had to replace "source" command with . because of sh issues when trying to migrate to docker
# run this script in your home directory by typing bash ./Install_openvino.sh
# after installing, it runs the c based face detect sample when finished but you will need a face.jpg image
# in you home directory before you run this script

# export DEBIAN_FRONTEND="noninteractive"
sudo dpkg --add-architecture armhf
echo "Updating base OS..."
sudo apt-get update && sudo apt-get upgrade -y
echo "Installing dependencies..."
sudo apt-get install -y build-essential cmake pkg-config wget lsb-release apt-utils libusb-1.0.0
# these next two lines should avoid getting a no space left on device error during install
sudo apt-get autoremove
sudo apt-get clean
# now install
echo "Downloading OpenVINO SDK..."
wget https://download.01.org/opencv/2019/openvinotoolkit/l_openvino_toolkit_raspbi_p_2019.1.094.tgz -O openvino.tgz
echo "Unpacking SDK..."
tar -xf openvino.tgz --strip 1 -C /opt/intel/openvino
echo "Setting installation directory path..."
sed -i "s|<INSTALLDIR>|/opt/intel/openvino|" /opt/intel/openvino/bin/setupvars.sh
echo "Setting up environment variables..."
sudo apt install cmake
# source /opt/intel/openvino/bin/setupvars.sh
source /opt/intel/openvino/bin/setupvars.sh
echo "source /opt/intel/openvino/bin/setupvars.sh" >> ~/.bashrc
echo "Setting up USB rules..."
sudo usermod -a -G users "$(whoami)"
echo "Activate Neural Stick 2 USB usage..."
sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh
echo "Testing installation using a face detector..."
cd /opt/intel/openvino/inference_engine/samples
mkdir build && cd build
echo "Making the test..."
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-march=armv7-a" /opt/intel/openvino/deployment_tools/inference_engine/samples
# if make crashes then change to -j2 instead of -j4
make -j2 object_detection_sample_ssd
echo "Downloading the face detector test support files..."
wget --no-check-certificate https://download.01.org/opencv/2019/open_model_zoo/R1/models_bin/face-detection-adas-0001/FP16/face-detection-adas-0001.bin
wget --no-check-certificate https://download.01.org/opencv/2019/open_model_zoo/R1/models_bin/face-detection-adas-0001/FP16/face-detection-adas-0001.xmlecho "Running the face detector test using the Neural Stick v2..."
./armv7l/Release/object_detection_sample_ssd -m face-detection-adas-0001.xml -d MYRIAD -i ~/image.jpg
echo "DONE!!"
