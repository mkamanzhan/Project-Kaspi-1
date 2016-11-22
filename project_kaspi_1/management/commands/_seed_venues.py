# -*- coding: utf-8 -*-
import requests
import math
import threading
import sys
import time

from project_kaspi_1.models import Venue
from project_kaspi_1.management.commands._fsq_settings import fsq_settings
from project_kaspi_1.dictionary import dictionary
class VenueSeeder:
	limit = fsq_settings['venue']['limit']

	url = fsq_settings['venue']['url']
	params = {
		'll': fsq_settings['venue']['ll'],
		'limit': fsq_settings['venue']['limit'],
		'radius': fsq_settings['venue']['radius'],
		'client_id': fsq_settings['client_id'],
		'client_secret': fsq_settings['client_secret'],
		'v':fsq_settings['v'],
	}

	total_results = 0

	process_count = 0

	success_count = 0
	success_venue_count = 0
	error_connection_count = 0
	error_decode_count = 0
	error_venue_exist = 0

	start_time = 0

	def seed(self):
		self.start_time = time.time()

		Venue.objects.all().delete()
		threads = []
		self.total_results = self.getTotalResults()

		self.total_pages = int(math.ceil(self.total_results/self.limit)) + 1
		for i in range(self.total_pages):
			threads.append(threading.Thread(target=self.parseUrl, args=(i,)))
		self.runThreads(threads)
		self.printResults()
	


	def printResults(self):
		print 'Venues added: ' + str(self.success_venue_count)
		print 'Parsed pages: ' + str(self.success_count)
		print 'Exist venues: ' + str(self.error_venue_exist)
		print 'Can\'t connect to Page: ' + str(self.error_connection_count)
		print 'Can\'t decode JSON:' + str(self.error_decode_count)
		print 'Execution time: {:.3f}'.format(time.time() - self.start_time) + 'sec'



	def runThreads(self, threads, thread_limit=20):
		process = 0.0
		length = len(threads)
		for i in range(length):
			if(i%thread_limit==0):
				for thread in threads[i-thread_limit:i]:
					thread.start()
					print str(int(process/length*100))+'%'
					sys.stdout.write("\033[F")
					

				for thread in threads[i-thread_limit:i]:
					thread.join()
					process += 1
					print str(int(process/length*100))+'%'
					sys.stdout.write("\033[F")

					
			elif(i == length-1):
				for thread in threads[(i/thread_limit)*thread_limit:i+1]:
					thread.start()
					print str(int(process/length*100))+'%'
					sys.stdout.write("\033[F")
				for thread in threads[(i/thread_limit)*thread_limit:i+1]:
					thread.join()
					process += 1
					print str(int(process/length*100))+'%'
					sys.stdout.write("\033[F")



	def getTotalResults(self):
		try:
			r = requests.get(self.url, params=self.params, timeout=5).json()
			return r['response']['totalResults']
		except:
			raise requests.exceptions.ConnectionError


	def parseUrl(self, offset):
		params = self.params
		params['offset'] = offset * self.limit
		try:
			r = requests.get(self.url, params=params, timeout=5).json()
			if(r['meta']['code'] == 200):
				for item in r['response']['groups'][0]['items']:
					self.saveVenue(item)
			self.success_count += 1
		except requests.exceptions.ConnectionError:
			self.error_connection_count += 1
		except ValueError:
			self.error_decode_count += 1
		self.process_count += 1



	def saveVenue(self,item):
		try:
			vid = item['venue']['id']
		except:
			vid = None

		try:
			name = item['venue']['name']
		except:
			name = None

		try:
			address = item['venue']['location']['address']
		except:
			address = None

		try:
			lat = item['venue']['location']['lat']
		except:
			lat = None

		try:
			lng = item['venue']['location']['lng']
		except:
			lng = None

		try:
			category = item['venue']['categories'][0]['name']
			if category in dictionary.keys():
				category = dictionary[category]
		except:
			category = None

		try:
			icon_url = item['venue']['categories'][0]['icon']['prefix'] + "512" + item['venue']['categories'][0]['icon']['suffix']
		except:
			icon_url = None

		try:
			Venue(
				vid = vid,
				name = name,
				address = address,
				category = category,
				lat = lat,
				lng = lng,
				tips = [],
				icon_url = icon_url
			).save()
			self.success_venue_count += 1
		except:
			self.error_venue_exist += 1
