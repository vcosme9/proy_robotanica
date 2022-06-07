
#importamos la bib ROS2 para python
import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus

from proy_robotanica_custom_interface.srv import TypeOfPlant

from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
import time

from proy_robotanica_custom_interface.srv import MyCameraMsg


#definimos la clase cliente
class Service(Node):
    def __init__(self):
        #constructor con el nombre del nodo
        super().__init__('servicio_nav_to_pose') 

        # tomate || berenjena
        self.tipo_planta = ""
        # declara el objeto servicio pasando como parametros
        # tipo de mensaje
        # nombre del servicio
        # callback del servicio
        self.srv = self.create_service(TypeOfPlant, '/service_nav_to_pose', self.service_nav_pose_callback)


        # Creamos el cliente de acciones de la navegacion a un punto
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
        if(abs(msg.pose.pose.position.x - self.goal_pose.pose.pose.position.x) < 0.25 and abs(msg.pose.pose.position.y - self.goal_pose.pose.pose.position.y) < 0.25):
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

    def service_nav_pose_callback(self, request, response):
        # recibe los parametros de esta clase
        #  recibe el mensaje request
        # devuelve el mensaje response
        
        self.get_logger().info(f'Se ha activado el servicio para: {request.type}')

        if request.type == "tomate":
            self.tipo_planta = request.type
            self.send_goal()
            # devuelve la respuesta
            response.success = True

        elif request.type == "berenjena":
            self.tipo_planta = request.type
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

        if(self.tipo_planta == "tomate"):
            # imprime mensaje informando del movimiento
            self.get_logger().info('Navegacion a los tomates')

            goal_pose = NavigateToPose.Goal()

            goal_pose.pose.header.frame_id = 'map'
            goal_pose.pose.pose.position.x= 1.0
            goal_pose.pose.pose.position.y= 1.0
            goal_pose.pose.pose.orientation.w= 1.0
           

        elif(self.tipo_planta == "berenjena"):
            # imprime mensaje informando del movimiento
            self.get_logger().info('Navegacion a las berenjenas')

            goal_pose = NavigateToPose.Goal()

            goal_pose.pose.header.frame_id = 'map'
            goal_pose.pose.pose.position.x= 4.0
            goal_pose.pose.pose.position.y= 2.0
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