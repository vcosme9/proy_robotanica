#importamos la bib ROS2 para python
from queue import Empty
import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose, FollowWaypoints
from action_msgs.msg import GoalStatus

from proy_robotanica_custom_interface.srv import Waypoints


#definimos la clase cliente
class Service(Node):
    def __init__(self):
        #constructor con el nombre del nodo
        super().__init__('servicio_nav_through_waypoints')

        # activate || deactivate
        self.activar = ""

        # declara el objeto servicio pasando como parametros
        # tipo de mensaje
        # nombre del servicio
        # callback del servicio
        self.srv = self.create_service(Waypoints, '/service_nav_through_waypoints', self.service_nav_waypoints_callback)


        # Creamos el cliente de acciones de la navegacion a un punto
        self._action_client = ActionClient(self, FollowWaypoints, 'navigate_through_waypoints')

    def service_nav_waypoints_callback(self, request, response):
        # recibe los parametros de esta clase
        #  recibe el mensaje request
        # devuelve el mensaje response

        if request.activate == "activate":
            self.activar = request.activate
            self.send_goal()
            # devuelve la respuesta
            response.success = True

        elif request.activate == "deactivate":
            self.activar = request.activate
            self.send_goal()
            # devuelve la respuesta
            response.success = True
       
        else:
            # estado de la respuesta
            # si no se ha dado ningun caso anterior
            response.success = False

        # devuelve la respuesta
        return response


    def send_goal(self):

        if(self.activar == "activate"):
            # imprime mensaje informando del movimiento
            self.get_logger().info('Navegacion por waypoints activado')

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
           

        elif(self.activar == "deactivate"):
            # imprime mensaje informando del movimiento
            self.get_logger().info('Navegacion por waypoints desactivado')

            goal_pose = NavigateToPose.Goal()

            goal_pose.pose.header.frame_id = 'map'
            goal_pose.pose.pose.position.x= 0.0
            goal_pose.pose.pose.position.y= 0.0
            goal_pose.pose.pose.orientation.w= 1.0

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
            #self.inicialize_capture_image()
            #rclpy.shutdown()
        else:
            if int(status) == 6:

                self.get_logger().info('---> Result: {0}'.format(status))

                self.send_goal()

            # Si el resultado=3 significa que el robot SI ha llegado al punto indicado

            if int(status) == 3:

                self.get_logger().info('---> Result: {0}'.format(status))

                self.get_logger().info('---> Initializing image capture')

                #self.inicialize_capture_image()
        

    #definimos la funcion de respuesta al feedback
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback))

    

def main(args=None):
    # inicializa la comunicacion ROS2
    rclpy.init(args=args)
    # creamos el nodo
    service = Service()
    try:
        #dejamos abierto el servicio
        rclpy.spin(service)
    except KeyboardInterrupt:
        service.get_logger().info('Cerrando el nodo service')
    finally:
        #destruimos el nodo
        service.destroy_node()
        #cerramos la comunicacion
        rclpy.shutdown()

#definimos el ejecutable
if __name__=='__main__':
    main()