#! /usr/bin/python

import rospy
from geometry_msgs.msg import *
from math import *
from nav_msgs.msg import *
from nav_msgs.srv import *
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


def generate_path(x,y,tol):
	rospy.wait_for_service('global_planner/planner/make_plan')
	try:	
		odom_act = rospy.wait_for_message('gazebo_odom',Odometry)	
		start = PoseStamped()
		x_act = odom_act.pose.pose.position.x
		y_act = odom_act.pose.pose.position.y
		start.header.frame_id='map'
		start.pose.position.x = x_act
		start.pose.position.y = y_act
		goal = PoseStamped()
		goal.header.frame_id='map'
		goal.pose.position.x = x
		goal.pose.position.y = y
		generate_plan = rospy.ServiceProxy('/global_planner/planner/make_plan', GetPlan)
		req = GetPlanRequest()
		start = start
		goal = goal
		tolerance = tol
        	generated_plan = generate_plan(start, goal, tolerance)
        	return generated_plan.plan
	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e


def callback(gx,gy,tol):
	path = 	generate_path(gx,gy,tol)
	poses = path.poses

	for i in range(1,len(poses),10) :	
		x, y = poses[i].pose.position.x, poses[i].pose.position.y
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
	rospy.init_node('lab_2_ex_1', anonymous=True)
	callback(int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]))
	



if __name__=='__main__':
	main_function()