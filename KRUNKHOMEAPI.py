"""
Support for an interface to work with a remote instance of Krunk Home Assistant.

If a connection error occurs while communicating with the API a
HomeAssistantError will be raised.
"""

import homeassistant.remote as remote
import time

api = remote.API('sample.com', 'password','8123')

def Start_Checkapi():	
	print()
	print('KrunkHome Control System')
	apicheck=str(remote.validate_api(api))
	print('API Check: '+apicheck)

def apicheck() -> bool:
	Start_Checkapi()
	if (str(remote.validate_api(api))=='ok'):
		call_mpd('picotts_say', 'Remote Access.',)
		print()
		time.sleep(1)
		return True
	elif (str(remote.validate_api(api))=='invalid_password'):
		print()
		print('K - Error: Check the API password')
		return False
	elif (str(remote.validate_api(api))=='cannot_connect'):
		print()
		print('K - Error: Check the API IP address')
		return False

def endscript():
	print()
	print('End of KrunkHome')
	
def get_config():
	print(remote.get_config(api))
	
def get_service():
	print('-- Available services:')
	services = remote.get_services(api)
	for service in services:
		print(service['services'])
		
def get_event():
	print('\n-- Available events:')
	events = remote.get_event_listeners(api)
	for event in events:
		print(event)
		
def get_entities():
	print('\n-- Available entities:')
	entities = remote.get_states(api)
	for entity in entities:
		print(entity)

def get_config_info():
	get_config()
	print()
	get_service()
	print()
	get_event()
	print()
	get_entities()
	print()

# Function Part

def turn_on(domain, switch_name):
	print('Turn on  - '+switch_name)
	remote.call_service(api, domain, 'turn_on', {'entity_id': '{}'.format(switch_name)})

def turn_off(domain, switch_name):
	print('Turn off - '+switch_name)
	remote.call_service(api, domain, 'turn_off', {'entity_id': '{}'.format(switch_name)})
	
def turn_on_all(domain):
	print('Turn on  all')
	remote.call_service(api, domain, 'turn_on')
	
def turn_off_all(domain):
	print('Turn off all')
	remote.call_service(api, domain, 'turn_off')
	
def call_mpd(service, message):
	print('Call TTS')
	remote.call_service(api, 'tts', service,{'entity_id': '{}'.format('media_player.mpd'), 'message': '{}'.format(message), })
	
def get_state(switch_name) -> str:
	return remote.get_state(api, switch_name)
