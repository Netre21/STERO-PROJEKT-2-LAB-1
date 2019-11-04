#! /usr/bin/python

import rospy
from geometry_msgs.msg import *
from math import *
from nav_msgs.msg import *
from tf.transformations import euler_from_quaternion


ANGULAR_VEL = 0.3
LINEAR_VEL = 0.3

hz = 50


pub = rospy.Publisher('/mux_vel_nav/cmd_vel', Twist , queue_size = 100) 

def theta_diff(x,y):
	odom_act = rospy.wait_for_message('/elektron/mobile_base_controller/odom',Odometry)
	x_act = odom_act.pose.pose.position.x
	y_act = odom_act.pose.pose.position.y

	roll , pitch, yaw = euler_from_quaternion([odom_act.pose.pose.orientation.x,odom_act.pose.pose.orientation.y,odom_act.pose.pose.orientation.z,odom_act.pose.pose.orientation.w])
	theta = atan2(y - y_act, x - x_act) - yaw
	return (x_act,y_act,theta)

def callback(data):
	poses = data.poses

	for i in poses :	
		x, y = i.pose.position.x, i.pose.position.y
		print x,y
		x_act,y_act,theta = theta_diff(x,y)

		distance = sqrt(pow((x_act - x), 2) + pow((y_act - y), 2))
		if (theta <= 0 and theta >= -3.14) or theta > 3.14:
			angular_movement = Vector3(0, 0, -ANGULAR_VEL)
		else:
			angular_movement = Vector3(0, 0, ANGULAR_VEL)
		
		linear_movement = Vector3(LINEAR_VEL, 0, 0)
		zero =  Vector3(0, 0, 0)

		#angular movement
		rate = rospy.Rate(hz)
		theta_old = theta
		while abs(theta_old) - abs(theta) > -0.001 or abs(theta) > 0.2:
			if abs(theta_old) > abs(theta) :
				theta_old = theta			
			_,_,theta = theta_diff(x,y)
			pub.publish(Twist(zero, angular_movement))		
			rate.sleep()
		pub.publish(Twist(zero, zero))

		#linear movement
		rate = rospy.Rate(hz)
		distance_old = distance
		while distance_old - distance > -0.05:		
			if distance_old > distance :			
				distance_old = distance
			x_act,y_act,_ = theta_diff(x,y)
			distance = sqrt(pow((x_act - x), 2) + pow((y_act - y), 2))
			pub.publish(Twist(linear_movement, zero))
			rate.sleep()	
		
		print "pos x ",x_act," pos y ",y_act
		pub.publish(Twist(zero, zero))
			



def main_function():
	rospy.init_node('lab_1_ex_2', anonymous=True)	
	sub = rospy.Subscriber('path_giver', Path, callback)
	rospy.spin()




if __name__=='__main__':
	main_function()