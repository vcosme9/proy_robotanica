from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='proy_robotanica_capture_image',
            executable='capturar',
            output='screen'
        ),
    ])
