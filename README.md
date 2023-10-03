# rbe595_p2b
Project 2b Fall 23 Aerial Robotics

## Overview:
You are provided a Jetson Orin Nano for running perception and motion planning algorithms. The motion commands are sent from Jetson to DJI Tello drone connected over WIFI.

## Instructions:
1. Jetson Orin Nano - Ubuntu Shell access without internet/ethernet/wifi setup

    - Connect the provided DC power adapter to Jetson Orin Nano and wait for a minute to boot up.

    - Connect a USB-C cable from host PC and Jetson Orin Nano. Use a serial terminal like gtkterm to gain shell access into Jetson.
    - Login using the user name and password (pasted on the Jetson board).
2. Jetson Orin Nano - Internet access

    With GUI:
    - Connect monitor, keyboard and mouse to Jetson.
    - Power up the unit and login.
    - Connect to WPI-Open and follow [these instructions](https://w.wpi.edu/) for setting up internet.

    Without GUI:
    - Use a wifi hotspot with some known password
    - Once you have shell access over USB, [follow this page](https://www.themakersphere.com/set-up-wifi-on-ubuntu/_) for setting wifi up

3. Jetson Orin Nano - Software Setup
    - Install [tensorflow](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html) and (or) [pytorch](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html) on Jetson board
    - Get SSH access up and running
    - You may additionally want to setup [vscode-server](https://code.visualstudio.com/docs/remote/vscode-server) for programming Jetson from host machine
    - Create a private repository on GitHub for storing your project codes. In case, the SSD on Jetson crashes, you may lose your code otherwise.

4. Tello Setup
    - Remove the propellers from Tello
    - Insert the battery and press the power button
    - You will see a open wifi hotspot with a unique ssid name (pasted on Tello drone)
    - Insert the additional wifi dongle into Jetson
    - Connect to the Tello's wifi hotspot using the wifi dongle. You will still have internet access in Jetson (from the inbuilt wifi antenna)
    - Clone this repository on Jetson
    - Install [DJItelloPy library](https://github.com/damiafuentes/DJITelloPy/tree/master/)
    - $python tello_sample.py
    - Check the outputs folder, make sure you are getting images from the drone
    - Attach the propellers and move on to flight testing