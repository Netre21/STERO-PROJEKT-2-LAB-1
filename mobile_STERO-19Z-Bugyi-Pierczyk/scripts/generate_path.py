#! /usr/bin/python


import rospy
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


def main_function():
	pub = rospy.Publisher('path_giver',Path,queue_size=10)
	rospy.init_node('generate_path', anonymous=True)
	
	path = Path()	
	
	path.header.stamp = rospy.Time.now()
	path.header.frame_id = 'base_link'
	path.header.seq = 1
	pose = generate_pose(-2,-0.5,1.3,1)
	path.poses.append(pose)
	pose = generate_pose(-1,-1,1.3,2)
	path.poses.append(pose)
	pose = generate_pose(-3,-3,1.3,3)
	path.poses.append(pose)
	pose = generate_pose(1,-2,1.3,4)
	path.poses.append(pose)
	
	pub.publish(path)	

if __name__=='__main__':
	main_function()