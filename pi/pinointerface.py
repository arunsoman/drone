import serial

def connect(uri='/dev/ttyACM0', brate=9600):
	ser = serial.Serial(uri, brate)
	def send(command):
		return
	def receive():
		return
	def disconnect():
		return
	return{'send':send, 'rec':receive}
