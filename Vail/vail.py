#!/usr/bin/env python

# Reguirements :
#	python >= 3.7.4
#	modules : aiohttp (pip install aiohttp)
#
# Note : currently decoding at 12wpm
#
#
print('vail.py script started')
import aiohttp
import asyncio
import json
import logging
import socket
import sys
import time
from datetime import date

LOGFILE = "vail.log"
LOGFORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=LOGFORMAT)

async def endpoint_check(endpoint):
	while True:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.ws_connect(endpoint) as ws:
					logging.info(f'Connection to {endpoint} succeeded')
					return
		except (NameError, aiohttp.client_exceptions.ClientError, IOError) as error:
			logging.error(error)
			await session.close()
			time.sleep(6)

async def vail_monitor():
	print(f'Vail Monitor has been started. Logging messages to {LOGFILE}')
	prev_clients_no = 0
	morse_time_unit = 71
	cw_end = 0
	traffic_file = 'traffic ' + str(date.today()) + '.txt'
	try:
		conn = aiohttp.TCPConnector(family = socket.AF_INET, ssl = False)
		async with aiohttp.ClientSession(connector = conn) as session:
			async with session.ws_connect("wss://vail.woozle.org/chat?repeater=General", protocols=["json.vail.woozle.org"]) as rws:
				async for msg in rws:
					jsontxt4file = str(msg)
					with open('json.txt', 'a') as f:
							f.write(jsontxt4file)
							f.write('\n')
					if msg.type == aiohttp.WSMsgType.TEXT:
						data = json.loads(msg.data)
						timestamp = data["Timestamp"]
						clients_no = data["Clients"]
						Duration_d = data["Duration"]
						if Duration_d == [] :
							if clients_no != prev_clients_no :
								print('Clients now connected: ', clients_no)
								traffic_file = 'traffic ' + str(date.today()) + '.txt'
								traffic_text = '\n'+ str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000)))  + ': ' +'Clients now connected: ' + str(clients_no)
								with open(traffic_file, 'a') as f:
									f.write(traffic_text)
							prev_clients_no = clients_no
						else:
							cw_start = data["Timestamp"]
							cw_duration = int(Duration_d[0])
							header = cw_start - cw_end
							cw_end = cw_start + cw_duration
							
							#Checking if newly received element is a DAH or a DIT
							if cw_duration > 2* morse_time_unit :
								morse_char_element = "-"
							else:
								morse_char_element = "."
							#Checking wether I should add a timestamp in the traffic file. (if 5 minutes have passed since last message)
							if header > 300000 :
								morse_message_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cw_start/1000)))  + ':' + '\n'
							else:
								morse_message_time = ''

							#Checking to see if the heading space means a new characted or a new word newly received element is a DAH or a DIT
							if header > 28 * morse_time_unit :
								morse_inter_element = '\n' + morse_message_time
							elif header > 7 * morse_time_unit :
								morse_inter_element = "   "
							elif header > 2.5 * morse_time_unit :
								morse_inter_element = " "
							else:
								morse_inter_element = ""
							traffic_text = morse_inter_element + morse_char_element
							with open(traffic_file, 'a') as f:
								f.write(traffic_text)

	except asyncio.TimeoutError:
		logging.warning('Communication timeout')
		time.sleep(12)

async def main():
	while True:
		try:
			logging.info('Vail Monitor has started')
			tasks = asyncio.gather(
				endpoint_check("wss://vail.woozle.org/chat?repeater=General"),
				vail_monitor()
			)
			await tasks
			for task in tasks._children:
				if task.exception() is not None:
					logging.error(f"Exception occurred: {task.exception()}")
		except aiohttp.ClientError as e:
			logging.error(e)
			time.sleep(6)
		except KeyboardInterrupt:
			sys.exit(0)

asyncio.run(main())
