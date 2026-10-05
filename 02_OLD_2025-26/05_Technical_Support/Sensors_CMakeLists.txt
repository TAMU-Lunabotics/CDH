cmake_minimum_required(VERSION 3.5)
project(sensors)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(imu_talker src/imu_publisher.cpp)
add_executable(imu_raw src/imu_raw_pub.cpp)

ament_target_dependencies(imu_talker rclcpp sensor_msgs)
ament_target_dependencies(imu_raw rclcpp sensor_msgs )

install(TARGETS
  imu_talker
  imu_raw
  DESTINATION lib/${PROJECT_NAME})

ament_package()
