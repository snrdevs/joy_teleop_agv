# Logitech F710 Ros Controller

## Introduction

This package subscribes `/joy` topic, and publishes `/cmd_vel` Twist commands. This package is configured for, differential drive mobile robot. You ay configure it for your needs. 

This package is configured for Logitech F710 Blueetooth Controller. 

## Instructions 

* Please install ros-[your_ros_version]-joy package:
  * Example: `sudo apt-get ros-melodic-joy` 
* Locate your connected joystick port: 
  * Example `ls /dev/input/ | grep js `
* Edit parameters located in `launch/teleop.launch` for your specifications. 



