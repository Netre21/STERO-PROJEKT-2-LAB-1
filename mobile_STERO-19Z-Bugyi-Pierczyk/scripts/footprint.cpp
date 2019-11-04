#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Polygon.h"
#include "geometry_msgs/Point32.h"

int main(int argc, char **argv)
{
ros::init(argc, argv, "footprint");
ros::NodeHandle n;
ros::Publisher publisher = n.advertise<geometry_msgs::Polygon>("/footprint", 1000);
ros::Rate loop_rate(10);

geometry_msgs::Polygon polygon;
//rozmiar elektrona zmierzony w rviz to
// szerokość 0.35m
// długość 0.56m

polygon.points.reserve(4);

geometry_msgs::Point32 t1;
t1.x = 0.3;
t1.y = 0.2;
polygon.points.push_back(t1);

geometry_msgs::Point32 t2;
t2.x = 0.3;
t2.y = -0.2;
polygon.points.push_back(t2);

geometry_msgs::Point32 t3;
t3.x = -0.3;
t3.y = -0.2;
polygon.points.push_back(t3);

geometry_msgs::Point32 t4;
t4.x = -0.3;
t4.y = 0.2;
polygon.points.push_back(t4);



while (ros::ok())
{
	publisher.publish(polygon);	
	ros::spinOnce();
	loop_rate.sleep();
}

return 0;

}