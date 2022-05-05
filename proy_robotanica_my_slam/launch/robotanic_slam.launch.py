#proy_robotanica_my_slam.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import SetEnvironmentVariable
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        #SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM','1'),
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[
                '-configuration_directory', get_package_share_directory('proy_robotanica_my_slam') + '/config',
                '-configuration_basename','proy_robotanica_my_slam.lua'
            ],
        ),
        Node(
            package='cartographer_ros',
            executable='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments = ['-resolution','0.05','-publish_period_sec','1.0']
        ),
    ]) 
