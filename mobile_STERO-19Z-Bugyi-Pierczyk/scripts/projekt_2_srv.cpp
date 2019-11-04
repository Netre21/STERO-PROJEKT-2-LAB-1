#include "ros/ros.h"
#include "geometry_msgs/PoseStamped.h"
#include <tf2_ros/transform_listener.h>
#include <costmap_2d/costmap_2d_ros.h>
#include <stero_mobile_init/Service.h>


tf2_ros::Buffer tfBuffer;

costmap_2d::Costmap2DROS * global_costmap;
tf2_ros::TransformListener * global_tf_listener;

costmap_2d::Costmap2DROS * local_costmap;
tf2_ros::TransformListener * local_tf_listener;

bool move_robot(stero_mobile_init::Service::Request &req,
				stero_mobile_init::Service::Response &res)
{
	res.result="ergergerg";
	ROS_INFO("Zakonczylem prace");
	//while(true)
	//{
	//local_costmap->updateMap();
	//ROS_INFO("jetsdem w petli");
	//}
  	return true;
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "integration_node_server");
	ros::NodeHandle n;
	ros::ServiceServer service = n.advertiseService("integration_node", move_robot);
	
	if(true)
	{
    global_tf_listener = new tf2_ros::TransformListener(tfBuffer);
	global_costmap = new costmap_2d::Costmap2DROS("global_costmap", tfBuffer);
	}


	if(true)
	{
    local_tf_listener = new tf2_ros::TransformListener(tfBuffer);
	local_costmap = new costmap_2d::Costmap2DROS("local_costmap", tfBuffer);
	//local_costmap->start();
	}	
	ROS_INFO("Ready to move robot."); 

	ros::spin();

	return 0;
}