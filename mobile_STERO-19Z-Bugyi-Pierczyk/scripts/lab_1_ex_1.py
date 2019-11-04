#! /usr/bin/python

import rospy
from geometry_msgs.msg import *
from math import *

ANGULAR_VEL = 0.1
LINEAR_VEL = 0.3

hz = 50


pub = rospy.Publisher('/mux_vel_nav/cmd_vel', Twist , queue_size = 100) 


def callback(data):
	x, y = data.position.x, data.position.y

	theta = atan2(y, x)
	distance = sqrt(pow(x, 2) + pow(y, 2))

	angular_time = theta / ANGULAR_VEL
	linear_time = distance / LINEAR_VEL

	angular_movement = Vector3(0, 0, ANGULAR_VEL)
	linear_movement = Vector3(LINEAR_VEL, 0, 0)
	zero =  Vector3(0, 0, 0)

	#angular movement
	rate = rospy.Rate(hz)
	i = 0
	while i < angular_time * hz:
		i = i + 1
		pub.publish(Twist(zero, angular_movement))
		rate.sleep()

	pub.publish(Twist(zero, zero))

	#linear movement
	rate = rospy.Rate(hz)
	i = 0
	while i < linear_time * hz:
		i = i + 1
		pub.publish(Twist(linear_movement, zero))
		rate.sleep()	

	pub.publish(Twist(zero, zero))
		



def main_function():
	rospy.init_node('lab_1_ex_1', anonymous=True)	
	sub = rospy.Subscriber('pose_giver', Pose, callback)
	rospy.spin()




if __name__=='__main__':
	main_function()