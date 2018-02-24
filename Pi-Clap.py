import pyaudio
import sys
import threading
import time
from time import sleep
from array import array
import KRUNKHOMEAPI as kapi
import homeassistant.remote as koapi #You will need to download homeassistant python api

def main():
	kapi.api=koapi.API('sample.com', 'password','8123') # HA-API:domain, password, port
	check=kapi.apicheck()
	if check:
		start()
	kapi.endscript()

clap = 0
wait = 1
flag = 0
pin = 24
exitFlag = False	

def toggleLight(c):
	domain = 'light' #domain
	switch_name = 'light.lamp' #switch name
	print (str(kapi.get_state(switch_name)))
	lamp=kapi.get_state(switch_name)
	if (lamp.state=='off'):
		kapi.turn_on(domain,switch_name)
	else:
		kapi.turn_off(domain,switch_name)
	sleep(1)
	print("Light toggled")

def waitForClaps(threadName):
	global clap
	global flag
	global wait
	global exitFlag
	global pin
	print ("Waiting for more claps")
	sleep(wait)
	if clap == 2:
		print ("Two claps")
		toggleLight(pin)
	# elif clap == 3:
	# 	print "Three claps"
	#elif clap == 4:
	#	exitFlag = True
	print ("Claping Ended")
	clap = 0
	flag = 0

def start():
	global clap
	global flag
	global pin

	chunk = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	threshold = 3000
	max_value = 0
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS, 
					rate=RATE, 
					input=True,
					output=True,
					frames_per_buffer=chunk)
	try:
		print ("Start")
		while True:
			data = stream.read(chunk)
			as_ints = array('h', data)
			max_value = max(as_ints)
			if max_value > threshold:
				clap += 1
				print ("Clapped")
			if clap == 1 and flag == 0:
				t=threading.Thread( target=waitForClaps, args=("waitThread",) )
				t.start()
				flag = 1
			if exitFlag:
				sys.exit(0)
	except (KeyboardInterrupt, SystemExit):
		print ("\rExiting")
		stream.stop_stream()
		stream.close()
		p.terminate()

if __name__ == '__main__':
	main()

