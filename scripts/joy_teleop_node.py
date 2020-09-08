#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy 
import rosgraph 
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import os

# Please install : sudo apt-get install ros-melodic-joy first to use this software, Please use the device in DI mode. Please work with "Mode" light closed otherwise Analog inputs will not work. 
# Coded by Hasan Şener - snrdevs@outlook.com 
# 2020 - Sep 

class JoyTeleop(): 
    def __init__(self): 
        #init node 
        rospy.init_node('joy_teleop')
        self.frequency = rospy.Rate(20)

        #create subscriber object 
        self.joy_subber = rospy.Subscriber('joy',Joy,callback=self.joy_sub)

        #create publisher object 
        self.twist_pubber = rospy.Publisher('cmd_vel',Twist,queue_size=1) 
        
        #get joystick parameter 
        self.joy_port_param_        = str(rospy.get_param("/joy_teleop_node/joystick_port"))
        self.agv_max_lin_vel        = float(rospy.get_param("/joy_teleop_node/agv_max_linear_velocity"))
        self.agv_max_ang_vel        = float(rospy.get_param("/joy_teleop_node/agv_max_angular_velocity"))
        self.twist_command = Twist() 

       

        #check if its connected 
        path_dir_ = '/dev/input/' + self.joy_port_param_
        if (os.path.exists(path_dir_)): 
            rospy.loginfo('Joystick connected at {}, advertising to /cmd_vel topic'.format(self.joy_port_param_))
        else: 
            rospy.logerr('Could not connect to joystick at port {} !'.format(self.joy_port_param_))
         
        #create Joystick Analog & Push Buttons 
        self.analog_left_vertical = 0.0  #LINEAR X COMMAND
        self.analog_left_horizontal = 0.0 
        
        self.analog_right_vertical= 0.0  #ANGULAR Z COMMAND
        self.analog_right_horizontal = 0.0 

        self.btn_x = 0 
        self.btn_y = 0
        self.btn_a = 0 
        self.btn_b = 0  

        self.back = 0
        self.start = 0 

        self.rb = 0 
        self.rt = 0

        self.lb = 0 
        self.lt = 0 

        self.main() 
        
    def joy_sub(self,data):
        asd = Joy() 
        
        self.analog_left_horizontal         = data.axes[0]
        self.analog_left_vertical           = data.axes[1]

        self.analog_right_horizontal        = data.axes[2]
        self.analog_right_vertical          = data.axes[3]
        
        self.btn_x  = data.buttons[0]
        self.btn_a  = data.buttons[1]       
        self.btn_b  = data.buttons[2]
        self.btn_y  = data.buttons[3]
        
        self.back   = data.buttons[8]
        self.start  = data.buttons[9]

        self.rb     = data.buttons[5]
        self.rt     = data.buttons[8]

        self.lb     = data.buttons[4] 
        self.lt     = data.buttons[6]

    def main(self):
        while (not(rospy.is_shutdown()) and rosgraph.is_master_online()): 
            if self.btn_b == 1: 
                self.twist_command.linear.x = 0
                self.twist_command.angular.z = 0 
                self.twist_pubber.publish(self.twist_command) 
            elif self.btn_b == 0: 
                linear_x_com    = round(self.analog_left_vertical * self.agv_max_lin_vel,3) 
                angular_z_com   = round(self.analog_right_horizontal * self.agv_max_ang_vel,3)  

                self.twist_command.linear.x = linear_x_com 
                self.twist_command.angular.z = angular_z_com 
                self.twist_pubber.publish(self.twist_command) 
            
            self.frequency.sleep() 

if __name__ == "__main__":
   my_joystick_node = JoyTeleop() 
