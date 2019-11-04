#! /usr/bin/python

import rospy
from geometry_msgs.msg import *
from math import *
from nav_msgs.msg import *
from tf.transformations import euler_from_quaternion

x_ele = 0
y_ele = 0
theta_ele = 0

pub = rospy.Publisher('odom_errors', Pose2D , queue_size = 100) 

def callback_gz(data):
	global x_ele
	global y_ele
	global theta_ele
	roll , pitch, yaw = euler_from_quaternion([data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w])
	x_ele = data.pose.pose.position.x	
	y_ele = data.pose.pose.position.y
	theta_ele = yaw
	
			
def callback_ele(data):
	
	roll , pitch, yaw = euler_from_quaternion([data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w])
	pose2d = Pose2D()
	pose2d.x = data.pose.pose.position.x - x_ele	
	pose2d.y = data.pose.pose.position.y - y_ele
	pose2d.theta = yaw - theta_ele
	print 'theta ', theta_ele, ' pos x ', x_ele ,' pos y ', y_ele
	pub.publish(pose2d)

def main_function():
	rospy.init_node('lab_1_ex_2', anonymous=True)	
	sub_gz = rospy.Subscriber('gazebo_odom', Odometry, callback_gz)
	sub_ele = rospy.Subscriber('elektron/mobile_base_controller/odom', Odometry, callback_ele)
	rospy.spin()




if __name__=='__main__':
	main_function()