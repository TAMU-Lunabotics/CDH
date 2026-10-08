from setuptools import setup

setup(
    name='cdh_actuator_guard',
    version='0.1.0',
    packages=['cdh_actuator_guard'],
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/cdh_actuator_guard']),
        ('share/cdh_actuator_guard',['package.xml','README.md']),
        ('share/cdh_actuator_guard/launch',['launch/guarded_drivers.launch.py']),
    ],
    entry_points={'console_scripts':[
        'roboclaw_guard = cdh_actuator_guard.ros_roboclaw:main',
        'pico_guard = cdh_actuator_guard.ros_pico:main',
    ]},
)
