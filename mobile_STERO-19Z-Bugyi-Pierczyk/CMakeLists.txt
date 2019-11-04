cmake_minimum_required(VERSION 3.5)
project(stero_mobile_init)
set(CMAKE_CXX_STANDARD 11)

find_package(catkin REQUIRED COMPONENTS
	rospy
	roscpp
	std_msgs
	geometry_msgs
	message_generation
	tf
	costmap_2d
	global_planner
	kdl_conversions
	base_local_planner
	clear_costmap_recovery
	rotate_recovery
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_service_files(
	FILES
	Service.srv
)

generate_messages(
	DEPENDENCIES
	std_msgs
	geometry_msgs
)

catkin_package(
#   INCLUDE_DIRS include
   LIBRARIES ${PROJECT_NAME}
   CATKIN_DEPENDS message_runtime
   DEPENDS elektron
)

install (DIRECTORY worlds/ DESTINATION share/${CMAKE_PROJECT_NAME}/worlds 
         FILES_MATCHING PATTERN "*.world")
install (DIRECTORY launch/ DESTINATION share/${CMAKE_PROJECT_NAME}/launch 
         FILES_MATCHING PATTERN "*.launch*")
install (DIRECTORY config/ DESTINATION share/${CMAKE_PROJECT_NAME}/config 
         FILES_MATCHING PATTERN "*.yaml")

add_executable(footprint scripts/footprint.cpp)
target_link_libraries(footprint ${catkin_LIBRARIES})
add_executable(integration_node_server scripts/projekt_2_srv.cpp)
target_link_libraries(integration_node_server ${catkin_LIBRARIES})
