import pinointerface as ch

def caliberate(alignment):
	return [20,20,20]

def start():	
	ch.connect()
	alignment = ch.receive()
	ch.send(caliberate(alignment))
	ch.disconnect()

start()