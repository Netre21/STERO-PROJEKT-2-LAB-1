#! /usr/bin/python


import rospy
import sys
import tf.transformations
from nav_msgs.msg import *
from geometry_msgs.msg import *

def generate_pose(x,y,theta,id_seq):
	pose = PoseStamped()
	
	pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = "base_link"
	pose.header.seq = id_seq        
	pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0

        quaternion = tf.transformations.quaternion_from_euler(0, 0, theta)
        pose.pose.orientation.x = quaternion[0]
        pose.pose.orientation.y = quaternion[1]
        pose.pose.orientation.z = quaternion[2]
        pose.pose.orientation.w = quaternion[3]
	return pose


def main_function(number_of_test):
	pub = rospy.Publisher('path_giver',Path,queue_size=10)
	rospy.init_node('generate_path', anonymous=True)
	
	path = Path()	
	
	path.header.stamp = rospy.Time.now()
	path.header.frame_id = 'base_link'
	path.header.seq = 1
	
	if number_of_test == 1 : #square
		pose = generate_pose(2,0,1.3,1)
		path.poses.append(pose)
		pose = generate_pose(2,-2,1.3,2)
		path.poses.append(pose)
		pose = generate_pose(0,-2,1.3,3)
		path.poses.append(pose)
		pose = generate_pose(0,0,1.3,4)
		path.poses.append(pose)
	if number_of_test == 2 : #front
		pose = generate_pose(2,0,1.3,1)
		path.poses.append(pose)
	if number_of_test == 3 : # rotation
		pose = generate_pose(0,-0.01,1.3,3)
		path.poses.append(pose)
	if number_of_test == 4 : # calibrate
		pose = generate_pose(1,0,1.3,3)
		path.poses.append(pose)
	pub.publish(path)	

if __name__=='__main__':
	provided_number = float(sys.argv[1])
	print provided_number,' huehue'
	if provided_number > 0 and provided_number < 5:
 		main_function(provided_number)
	else:
		print 'number must be in range 1-4'
