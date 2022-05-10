#action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import time


class NavigationToPose(Node):

    def __init__(self):
        super().__init__('waypoint_client')
        #creamos el objeto cliente de una accion
        #con parametros
        #nodo
        #tipo de mensaje
        #nombre de la accion
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        

    #definimos la funcion de mandar goal
    def send_goal(self, goal_pose):
        # crea el mensaje tipo Goal
        # y lo rellena con el argumento dado
        # Rellena con la posicion (int) del punto al que quiere ir (int)
        
	    #espera a que el servidor este listo
        self._action_client.wait_for_server()
        # envia el goal
        self._send_goal_future = self._action_client.send_goal_async(goal_pose,feedback_callback=self.feedback_callback)
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
            self.get_logger().info('----------tipo resultado: {0}'.format(type(status)))
            self.get_logger().info('Result: {0}'.format(status))
            self.send_goal()
        

    #definimos la funcion de respuesta al feedback
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback))

    

def main(args=None):
    rclpy.init(args=args)

    pose = NavigateToPose.Goal()
    pose.pose.header.frame_id = 'map'
    pose.pose.pose.position.x= 5.0
    pose.pose.pose.position.y= 0.0
    pose.pose.pose.orientation.w= 1.0

    action_client = NavigationToPose(pose)
    future = action_client.send_goal()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
