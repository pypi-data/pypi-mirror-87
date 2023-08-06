#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *

# the synchronize users thread (synchs once per hour).
class SynchronizeUsers(threading.Thread):
	def __init__(self, 
		# pass the r3stapi.RestAPI object.
		restapi=None,
		# show the daemon logs.
		silent=False,
		# the synchronize interval in minutes (default: synchronizes once per 60 min).
		synchronize_interval=60,
		# the sleep interval in minutes (default: checks synchronize interval once per 15 min).
		sleep_interval=15,
	):
		threading.Thread.__init__(self)
		self.restapi = restapi
		self.silent = silent
		self.synchronize_interval = synchronize_interval
		self.sleep_interval = sleep_interval
		self.monthly_requests, self.monthly_costs = self.get_costs(self.synchronize_interval, len(self.restapi.uid_api_keys))
		monthly_requests, costs = self.get_costs(self.synchronize_interval, 10000)
		print(f"Monthly daemon requests: {int(self.monthly_requests)}")
		print(f"Monthly daemon costs: € {self.monthly_costs:.2f}")
		print(f"Monthly daemon costs per 10.000 users: € {costs:.2f}")
	def run(self):
		last = None
		while True:
			date, new = Formats.Date(), False
			if last == None: new = True
			else:
				increased = date.increase(last, minutes=self.synchronize_interval)
				new = date.compare(increased, date.timestamp) in ["present", "past"]
			if new:
				last = date.timestamp
				response = self.restapi.synchronize_users(silent=self.silent)
				r3sponse.log(response, log_level=-1, save_errors=True)
			time.sleep(self.sleep_interval*60)
	def get_costs(self, synchronize_interval=None, total_users=None):
		monthly_requests = ( total_users * (( 60 * 24 ) / synchronize_interval )) * 30.5
		monthly_costs = monthly_requests * (0.06/100000)
		return monthly_requests, monthly_costs