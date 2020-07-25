import RPi.GPIO as GPIO

class Motor(object):
	
	def __init__(self, enPin, pin1, pin2):
		self.enPin = enPin
		self.pin1 = pin1
		self.pin2 = pin2
		GPIO.setup(self.enPin, GPIO.OUT)
		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)
		self.pwm = GPIO.PWM(self.enPin, 100)
		self.pwm.start(0)

	def forward(self, speed = 50):
		GPIO.output(self.enPin, False)
		GPIO.output(self.pin1, True)
		GPIO.output(self.pin2, False)
		self.pwm.ChangeDutyCycle(speed)
		GPIO.output(self.enPin, True)

        def backward(self, speed = 50):
		GPIO.output(self.enPin, False)
                GPIO.output(self.pin2, True)
                GPIO.output(self.pin1, False)
                self.pwm.ChangeDutyCycle(speed)
                GPIO.output(self.enPin, True)

        def stop(self):
                GPIO.output(self.pin1, False)
                GPIO.output(self.pin2, False)
                self.pwm.ChangeDutyCycle(0)
                GPIO.output(self.enPin, False)
	
	def clip(self, value, minimum, maximum):
		if value < minimum:
			return minimum
		elif value > maximum:
			return maximum
		else:
			return value

	def move(self, speed_percent):
		speed = self.clip(abs(speed_percent), 0, 100)
		if speed_percent < 0:
			self.backward(speed)
		else:
			self.forward(speed)
	
	def cleanup(self):
		self.pwm.stop()
