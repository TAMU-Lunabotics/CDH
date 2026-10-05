from setuptools import setup
import os
from glob import glob

package_name = 'drive'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lunabotics',
    maintainer_email='lunabotics@todo.todo',
    description='Tank drive with RoboClaw',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'tank_drive = drive.tank_drive:main',
            'pico_drive = drive.pico_drive:main',
            'auto_drive = drive.auto_drive:main',
            'auto_pub_test = drive.auto_pub_test:main',
            'camera = drive.camera:main',
            'pico_drive_encoders = drive.pico_drive_encoders:main',
            'tank_drive_uart = drive.tank_drive_uart:main',
        ],
    },
)