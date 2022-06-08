#action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
import time

from proy_robotanica_custom_interface.srv import MyCameraMsg

class FollowWaypoints(Node):

    def __init__(self):
        super().__init__('waypoint_client')
        #creamos el objeto cliente de una accion
        #con parametros
        #nodo
        #tipo de mensaje
        #nombre de la accion
        self.goal_pose = NavigateToPose.Goal()
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.req = MyCameraMsg.Request()

        #Variable que cambiara cuando llegue al goal estipulado
        self.isPosition = False

        # crear el objeto subscriptor
        # al topic /odom topic wcon una cola de 10 messages.
        # create_subscription(msg_type, topic, callback, qos_profile, callback_group, event_callbacks, raw)
        self.subscriber= self.create_subscription(
            Odometry,
            '/odom',
            self.comprobar_pos,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)) 
        # prevent unused variable warning
        self.subscriber      

    def comprobar_pos(self, msg):
        # imprime los datos leídos  
        self.get_logger().info('POS X: ' + str(msg.pose.pose.position.x) + 'POS Y: ' + str(msg.pose.pose.position.y))     
        if(abs(msg.pose.pose.position.x - self.goal_pose.pose.pose.position.x) < 0.5 and abs(msg.pose.pose.position.y - self.goal_pose.pose.pose.position.y) < 0.5):
            self.isPosition = True
            self.get_logger().info('Abriendo camara')
            client = self.create_client(MyCameraMsg, 'capturar')
            #crea el mensaje 
            self.future = client.call_async(self.req)
            #cada segundo revisa si el servicio esta activo
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('el servicio no esta activo, prueba de nuevo...')

        else:
            self.isPosition = False
            self.get_logger().info('No se ha llegado aun')

    #definimos la funcion de mandar goal
    def send_goal(self, goal_pose):
        self.goal_pose = goal_pose
	    #espera a que el servidor este listo
        self._action_client.wait_for_server()
        # envia el goal 
        self._send_goal_future = self._action_client.send_goal_async(goal_pose,feedback_callback=self.feedback_callback)
        #rclpy.spin_until_future_complete(self, self._send_goal_future)
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
            
            client = self.create_client(MyCameraMsg, 'capturar')
            
            #cada segundo revisa si el servicio esta activo
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('el servicio no esta activo, prueba de nuevo...')
            
            
            
            self.future = client.call_async(self.req)
            #rclpy.shutdown()
            
        else:
            if int(status) == 6:

                

                self.send_goal(self.goal_pose)

                

                
        

    #definimos la funcion de respuesta al feedback
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg

    
    
def main(args=None):
    rclpy.init(args=args)

    

    goal_pose = NavigateToPose.Goal()
    goal_pose.pose.header.frame_id = 'map'
    goal_pose.pose.pose.position.x= 2.0
    goal_pose.pose.pose.position.y= 0.0
    goal_pose.pose.pose.orientation.w= 1.0
    action_client = FollowWaypoints()
    future = action_client.send_goal(goal_pose)
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
