
from time import time
import rclpy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
import datetime

#Mensaje de camara
from proy_robotanica_custom_interface.srv import MyCameraMsg
#Para subir la imagen a s3
import logging
#import boto3
#from botocore.exceptions import ClientError
#from progresspercentage import ProgressPercentage
import os

class Ros2OpenCVImageConverter(Node):   

    def __init__(self):
        super().__init__('capturar')
        path = os.getcwd()
        print("Abriendo")
        self.bridge_object = CvBridge()
        print("Puente creado")
    
        self.srv = self.create_service(MyCameraMsg, 'capturar', self.service_callback)
        print("Servicio creado")
        

    def service_callback(self, request, response):
        image_sub = self.create_subscription(
            Image,'/camera/image_raw',
            self.camera_callback,
            QoSProfile(depth=10, 
            reliability=ReliabilityPolicy.RELIABLE))
        print("img hecho")
        response.success = True
        print("Callback servicio hecho")
        return response

    def camera_callback(self,data):
        print("Callback camara")
        try:
            # Seleccionamos bgr8 porque es la codificacion de OpenCV por defecto
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
            
            fecha=datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")+".jpg"
            cv2.imwrite("1.jpg", cv_image)
            #self.res=self.upload_file("/home/carlos/turtlebot3_ws/2.jpg","imagenesrobotanica") 
            print("imagen creada")
        except CvBridgeError as e:
            print(e)
        
        
        cv2.imshow("Imagen",cv_image)
        
          
        #res=self.upload_file("imagen_camara_"+dia+".jpg","imagenesrobotanica")   
        
        cv2.waitKey(0)  
        cv2.destroyAllWindows()

        return self.res

    def upload_file(inutil, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            # Versión sin info progreso
            response = s3_client.upload_file(file_name, bucket, object_name)
            # Versión con info progreso
            #response = s3_client.upload_file(file_name, bucket, object_name,Callback=ProgressPercentage(file_name))
        except ClientError as e:
            logging.error(e)
            return False
        return True

def main(args=None):

    rclpy.init(args=args)    
    img_converter_object = Ros2OpenCVImageConverter()    
       
    try:
        rclpy.spin(img_converter_object)
    except KeyboardInterrupt:
        img_converter_object.destroy_node()
        print("Fin del programa!")
    
    cv2.destroyAllWindows() 
    

if __name__ == '__main__':
    main()
