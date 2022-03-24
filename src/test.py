#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


robot_width = .5
lidar_y_position = .1
clearence = .2
R_value = (robot_width/2)/math.sin(math.radians(22.5))+lidar_y_position+clearence
Wall_width = 3

def move_right(data):
	pub = rospy.Publisher('twist_msg', Twist, queue_size = 10)
	msg = Twist()
    	linear_x = 0
    	angular_z = 0
    	state_description = ''
	a = data.ranges[147:233]
	if min(a) <= R_value+clearence:
		Left = 1
	else:
		Left = 0

	if Left == 1:
		state_description = 'Obstacle Detected_right'
		linear_x = 0.6
		angular_z = 0
	elif Left == 0:
		state_description = 'Clear'
		angular_z = -0.3
		linear_x = 0
	rospy.loginfo(state_description)
    	msg.linear.x = linear_x
    	msg.angular.z = angular_z
    	pub.publish(msg)

def move_left(data):
	pub = rospy.Publisher('twist_msg', Twist, queue_size = 10)
	msg = Twist()
    	linear_x = 0
    	angular_z = 0
    	state_description = ''
	a = data.ranges[522:617]
	if min(a) <= R_value+clearence:
		Right = 1
	else:
		Right = 0

	if Right == 1:
		state_description = 'Obstacle Detected_left'
		linear_x = 0.6
		angular_z = 0
	elif Right == 0:
		state_description = 'Clear'
		angular_z = 0.3
	rospy.loginfo(state_description)
    	msg.linear.x = linear_x
    	msg.angular.z = angular_z
    	pub.publish(msg)

def move_straight():
	pub = rospy.Publisher('twist_msg', Twist)
	msg = Twist()
    	linear_x = 0.6
    	angular_z = 0
    	state_description = 'Clear_straight'
	rospy.loginfo(state_description)
    	msg.linear.x = linear_x
    	msg.angular.z = angular_z
    	pub.publish(msg)

def callback(data):
   	a = data.ranges[48:95]
    	if min(a) <= R_value:
        	Left = 1
    	else:
        	Left = 0
    	b = data.ranges[0:47]
    	if min(b) <= R_value:
        	Front_left = 1
    	else:
        	Front_left = 0
    	c = data.ranges[713:760]
    	if min(c) <= R_value:
        	Front_right = 1
    	else:
        	Front_right = 0
    	d = data.ranges[665:713]
    	if min(d) <= R_value:
        	Right = 1
    	else:
        	Right = 0



#-------

	if Left == 0 and Front_left == 0 and Front_right == 0 and Right == 0:
        	state_description = 'case 1 - clear'
       		move_straight()
        elif Left == 1 and Front_left == 0 and Front_right == 0 and Right == 0:
        	state_description = 'case 2 - far_left'
		move_right(data)
    	elif Left == 0 and Front_left == 1 and Front_right == 0 and Right == 0:
        	state_description = 'case 3 - front_left'
        	move_right(data)
        elif Left == 1 and Front_left == 1 and Front_right == 0 and Right == 0:
        	state_description = 'case 4 - left'
        	move_right(data)
        elif Left == 0 and Front_left == 0 and Front_right == 0 and Right == 1:
        	state_description = 'case 5 - far_right'
        	move_left(data)
    	elif Left == 0 and Front_left == 0 and Front_right == 1 and Right == 0:
        	state_description = 'case 6 - front_right'
        	move_left(data)
        elif Left == 0 and Front_left == 0 and Front_right == 1 and Right == 1:
        	state_description = 'case 7 - right'
        	move_left(data)
        elif Left == 0 and Front_left == 1 and Front_right == 1 and Right == 0:
        	state_description = 'case 8 - front'
        	move_right(data)
        elif Left == 1 and Front_left == 0 and Front_right == 0 and Right == 1:
        	state_description = 'case 9 - far_left/far_right'
        	move_left(data)
    	elif Left == 1 and Front_left == 0 and Front_right == 1 and Right == 0:
        	state_description = 'case 10 - far_left/front_right'
        	move_left(data)
        elif Left == 0 and Front_left == 1 and Front_right == 0 and Right == 1:
        	state_description = 'case 11 - front_left/far_right'
        	move_left(data)
        elif Left == 0 and Front_left == 1 and Front_right == 1 and Right == 1:
        	state_description = 'case 12 - front_left/right'
        	move_left(data)
        elif Left == 1 and Front_left == 1 and Front_right == 1 and Right == 0:
        	state_description = 'case 13 - left/front_right'
        	move_right(data)
        elif Left == 1 and Front_left == 0 and Front_right == 1 and Right == 1:
        	state_description = 'case 14 - far_left/right'
        	move_left(data)
    	elif Left == 1 and Front_left == 1 and Front_right == 0 and Right == 1:
        	state_description = 'case 15 - left/far_right'
        	move_left(data)
        elif Left == 1 and Front_left == 1 and Front_right == 1 and Right == 1:
        	state_description = 'case 16 - all_directions'
        	move_left(data)
        else:
        	state_description = 'unknown case'



rospy.init_node('check_obstacle')

rospy.Subscriber('/scan', LaserScan, callback)

rospy.spin()
