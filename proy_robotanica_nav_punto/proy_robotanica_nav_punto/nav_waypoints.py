#action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import time


class FollowWaypoints(Node):

    def __init__(self):
        super().__init__('waypoint_client')
        #creamos el objeto cliente de una accion
        #con parametros
        #nodo
        #tipo de mensaje
        #nombre de la accion
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        

    #definimos la funcion de mandar goal
    def send_goal(self, goal_poses):
        # crea el mensaje tipo Goal
        # y lo rellena con el argumento dado
        # Rellena con la posicion (int) del punto al que quiere ir (int)
        
	    #espera a que el servidor este listo
        self._action_client.wait_for_server()
        # envia el goal
        self._send_goal_future = self._action_client.send_goal_async(goal_poses,feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self, self.send_goal_future)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    #definimos la funcion de respuesta al goal
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    
    #definimos la funcion de respuesta al resultado
    def get_result_callback(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Navigation_Succeded')
            rclpy.shutdown()
        else:
            self.get_logger().info('Result: {0}'.format(status))
            self.send_goal()
        

    #definimos la funcion de respuesta al feedback
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback))

    

def main(args=None):
    rclpy.init(args=args)

    # Array con posiciones
    goal_poses = []

    # Waypoint 1
    goal_pose_1 = NavigateToPose.Goal()
    goal_pose_1.pose.header.frame_id = 'map'
    goal_pose_1.pose.pose.position.x= 5.0
    goal_pose_1.pose.pose.position.y= 0.0
    goal_pose_1.pose.pose.orientation.w= 1.0
    goal_poses.append(goal_pose_1)
    # Waypoint 2
    goal_pose_2 = NavigateToPose.Goal()
    goal_pose_2.pose.header.frame_id = 'map'
    goal_pose_2.pose.pose.position.x= 5.0
    goal_pose_2.pose.pose.position.y= 0.0
    goal_pose_2.pose.pose.orientation.w= 1.0
    goal_poses.append(goal_pose_2)
    # Waypoint 3
    goal_pose_3 = NavigateToPose.Goal()
    goal_pose_3.pose.header.frame_id = 'map'
    goal_pose_3.pose.pose.position.x= 5.0
    goal_pose_3.pose.pose.position.y= 0.0
    goal_pose_3.pose.pose.orientation.w= 1.0
    goal_poses.append(goal_pose_3)
    # Waypoint 4
    goal_pose_4 = NavigateToPose.Goal()
    goal_pose_4.pose.header.frame_id = 'map'
    goal_pose_4.pose.pose.position.x= 5.0
    goal_pose_4.pose.pose.position.y= 0.0
    goal_pose_4.pose.pose.orientation.w= 1.0
    goal_poses.append(goal_pose_4)
    

    action_client = FollowWaypoints(goal_poses)
    future = action_client.send_goal()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
