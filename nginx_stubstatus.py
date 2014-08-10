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

from collectors.lib import utils

COLLECTION_INTERVAL = 15

STATUS_URL = "http://localhost/status"
METRIC_BASENAME = "nginx.stubstatus"

def main():
	utils.drop_privileges()

	while True:
		response =  requests.get(STATUS_URL)
		timestamp = int(time.time())
		lines = [ l.strip() for l in response.text.split("\n") ][:-1]

		print "%s.conn.active %d %s" %(METRIC_BASENAME, timestamp, lines[0].split(":")[-1].strip())

		(cAccepted, cHandled, cHandles) = ( i for i in lines[2].split() if i != "")
		print "%s.conn.accepted %d %s" %(METRIC_BASENAME, timestamp, cAccepted)
		print "%s.conn.handled %d %s" %(METRIC_BASENAME, timestamp, cHandled)
		print "%s.conn.handles %d %s" %(METRIC_BASENAME, timestamp, cHandles)

		(_, reqReads, _, reqWrites, _, reqWaiting)= (c.strip() for c in lines[-1].split())
		print "%s.request %d %s state=reading" %(METRIC_BASENAME, timestamp, reqReads)
		print "%s.request %d %s state=writing" %(METRIC_BASENAME, timestamp, reqWrites)
		print "%s.request %d %s state=waiting" %(METRIC_BASENAME, timestamp, reqWaiting)

		sys.stdout.flush()
		time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
	sys.stdin.close()
	sys.exit(main())