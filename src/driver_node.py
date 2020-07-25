#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO
from time import sleep
from motor import Motor

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class Driver(object):
	def __init__(self):
		rospy.init_node("driver")
		
		self._last_received = rospy.get_time()
		self._timeout = rospy.get_param("~timeout", 2)
		self._rate = rospy.get_param("~rate", 10)
		self._max_speed = rospy.get_param("~max_speed", 0.5)
		self._wheel_base = rospy.get_param("~wheel_base", 0.091)

		self._rMotor = Motor(12, 10,8)
		self._lMotor = Motor(7,3,5)
		self._rMotor_speed = 0
		self._lMotor_speed = 0

		rospy.Subscriber("cmd_vel", Twist, self._velocity_received_callback)
		
	def _velocity_received_callback(self, message):
		self._last_received = rospy.get_time()

		linear = message.linear.x
		angular = message.angular.z

		lSpeed = linear - angular*self._wheel_base/2
		rSpeed = linear + angular*self._wheel_base/2

		self._lMotor_speed = 100 * lSpeed/self._max_speed
		self._rMotor_speed = 100 * rSpeed/self._max_speed

	def run(self):
		rate = rospy.Rate(self._rate)
		
		while not rospy.is_shutdown():
			delay = rospy.get_time() - self._last_received
			if delay < self._timeout:
				self._rMotor.move(self._rMotor_speed)
				self._lMotor.move(self._lMotor_speed)
			else:
				self._rMotor.stop()
				self._lMotor.stop()
			rate.sleep()

	def exit(self):
		self._rMotor.cleanup()
		self._lMotor.cleanup()

def main():
	driver = Driver()
	
	# Run the driver
	driver.run()

	driver.exit()

	GPIO.cleanup()

if __name__ == "__main__":
	main()
