"""
Motor control launch file for Lunabotics hardware operation.

This launch file runs:
1. Pico drive node
2. Tank drive node (USB or UART)

Usage:
    ros2 launch drive drive.launch.py
    ros2 launch drive drive.launch.py using_uart:=true
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    using_uart = LaunchConfiguration('using_uart', default='false')
    return LaunchDescription([
        DeclareLaunchArgument(
            'using_uart',
            default_value='false',
            description='Use uart tank drive node instead of usb tank drive node'
        ),
        # pico
        Node(
            package='drive',
            executable='pico_drive',
            name='pico_drive',
            output='screen',
        ),
        # usb/serial roboclaw
        Node(
            package='drive',
            executable='tank_drive',
            name='tank_drive',
            output='screen',
            condition=UnlessCondition(using_uart),
        ),
        # uart roboclaw
        Node(
            package='drive',
            executable='tank_drive_uart',
            name='tank_drive',
            output='screen',
            condition=IfCondition(using_uart),
        ),
    ])