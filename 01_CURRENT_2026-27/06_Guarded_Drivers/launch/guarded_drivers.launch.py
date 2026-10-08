"""Independent CDH driver candidate. All hardware is disabled by default."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration as L
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    defaults = {
        'drive_hardware_enable':'false','tool_hardware_enable':'false',
        'protocol_confirmed':'false','drive_serial_port':'',
        'pico_serial_port':'','roboclaw_library_dir':'',
        'wheel_track_m':'0.0','full_power_speed_mps':'0.0',
        'left_sign':'0','right_sign':'0',
        'encoder_left_sign':'0','encoder_right_sign':'0',
        'swap_channels':'false','lift_down_sign':'0','lift_speed':'0.0',
    }

    def typed(name,typ):
        return ParameterValue(L(name),value_type=typ)

    return LaunchDescription([
        *[DeclareLaunchArgument(k,default_value=v) for k,v in defaults.items()],
        Node(package='cdh_actuator_guard',executable='roboclaw_guard',
             parameters=[{
                 'hardware_enable':typed('drive_hardware_enable',bool),
                 'serial_port':typed('drive_serial_port',str),
                 'roboclaw_library_dir':typed('roboclaw_library_dir',str),
                 'wheel_track_m':typed('wheel_track_m',float),
                 'full_power_speed_mps':typed('full_power_speed_mps',float),
                 'left_sign':typed('left_sign',int),
                 'right_sign':typed('right_sign',int),
                 'encoder_left_sign':typed('encoder_left_sign',int),
                 'encoder_right_sign':typed('encoder_right_sign',int),
                 'swap_channels':typed('swap_channels',bool),
             }],output='screen'),
        Node(package='cdh_actuator_guard',executable='pico_guard',
             parameters=[{
                 'hardware_enable':typed('tool_hardware_enable',bool),
                 'protocol_confirmed':typed('protocol_confirmed',bool),
                 'serial_port':typed('pico_serial_port',str),
                 'lift_down_sign':typed('lift_down_sign',int),
                 'lift_speed':typed('lift_speed',float),
             }],output='screen'),
    ])
