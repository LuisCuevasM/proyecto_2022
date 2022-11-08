#!/usr/bin/env python
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
from sensor_msgs.msg import Joy # impor mensaje tipo Joy
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from duckietown_msgs.msg import Twist2DStamped 
from geometry_msgs.msg import Twist
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
import cv2 # importar libreria opencv
import os     
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from cv_bridge import CvBridge # importar convertidor de formato de imagenes

class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		self.sub = rospy.Subscriber("/duckiebot/joy" , Joy, self.callback)
		self.Sub_Cam = rospy.Subscriber("/duckiebot/camera_node/image/rect", Image, self.tomar_img)
		self.publi = rospy.Publisher("duckiebot/wheels_driver_node/car_cmd", Twist2DStamped, queue_size = "x")
		self.twist = Twist2DStamped()
		self.i = 0
		self.x = 0
		self.y = 0
		self.z = 0
		
	def callback(self,msg):
		
		self.y = msg.buttons[3]
		self.x = msg.buttons[1]
		self.z = msg.buttons[2]
		print(self.y, self.x, self.z)
		if self.x == 1:
			self.twist.omega = self.x*5
		else:
			self.twist.omega = self.z*-5
		self.twist.v = self.y 

		self.publi.publish(self.twist)
		
         	#Se genera un archivo de texto para guardar velocidades
        	#archivo = open("vel.txt", "a") 		
         	#archivo.write( str(self.y) +',' +str(self.x) +','+ str(self.z) + '\n' ) 
		#archivo.close()
		
	def tomar_img(self, msg):
		bridge = CvBridge()
		image = bridge.imgmsg_to_cv2(msg, "bgr8") 
		#Se declara la carpeta donde se guardaran las imagenes (crear en la misma ruta que se encuentra recorder.py)
                path = 'duckietown/catkin_ws/src/desafios_2022/src'
                #Se escribe la imagen en la caperta del path
                nombre = "images/imagen" + str(self.i)+ ".jpg"
                cv2.imwrite(nombre, image)

                
                	#Se genera un archivo de texto para guardar velocidades
        	archivo = open("vel.txt", "a") 		
         	archivo.write(nombre +  ", "+ str(self.y) + ',' + str(self.x) + ',' + str(self.z)+'\n' ) 
		archivo.close()
		self.i+=1
		

def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
