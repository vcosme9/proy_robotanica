from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='proy_robotanica_services',
            executable='service_nav_to_pose',
            output='screen'
        ),
    ])
