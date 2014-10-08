#!/usr/bin/env python
'''
nginx_stubstatus.py

This uses nginx's stub_status module to get current nginx information.

nginx.stubstatus.conn.active				active connections
nginx.stubstatus.conn.accepted 				connections accepted
nginx.stubstatus.conn.handled 				connections handled
nginx.stubstatus.conn.handles 				open connection handles
nginx.stubstatus.request{state=reading} 	read requests
nginx.stubstatus.request{state=writing} 	write requests
nginx.stubstatus.request{state=waiting} 	requesting waiting
'''

import sys
import time
import requests

## tcollector library - 'tcollector/libs'
from collectors.lib import utils

COLLECTION_INTERVAL = 15

STATUS_URL = "http://localhost/status"
METRIC_BASENAME = "nginx.stubstatus"

def main():
	utils.drop_privileges()

	while True:

		try:
			response =  requests.get(STATUS_URL)
		except :
			time.sleep(COLLECTION_INTERVAL)
			continue
			
		timestamp = int(time.time())
		lines = [ l.strip() for l in response.text.split("\n") ][:-1]

		print "%s.conn.active %d %s" %(METRIC_BASENAME, timestamp, lines[0].split(":")[-1].strip())

		(cAccepts, cHandled, cRequests) = ( i for i in lines[2].split() if i != "")
		print "%s.conn.accepts %d %s" %(METRIC_BASENAME, timestamp, cAccepts)
		print "%s.conn.handled %d %s" %(METRIC_BASENAME, timestamp, cHandled)
		print "%s.requests %d %s" %(METRIC_BASENAME, timestamp, cRequests)

		(_, conReads, _, conWrites, _, conWaiting)= (c.strip() for c in lines[-1].split())
		print "%s.conn.state %d %s type=reading" %(METRIC_BASENAME, timestamp, conReads)
		print "%s.conn.state %d %s type=writing" %(METRIC_BASENAME, timestamp, conWrites)
		print "%s.conn.state %d %s type=waiting" %(METRIC_BASENAME, timestamp, conWaiting)

		sys.stdout.flush()
		time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
	sys.stdin.close()
	sys.exit(main())
