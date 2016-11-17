import requests
import math
import threading
import sys
import time

from project_kaspi_1.models import Venue

class VenueSeeder:
	limit = 50

	url = 'https://api.foursquare.com/v2/venues/explore'
	params = {
		'll': '43.2551,76.9126',
		'limit': limit,
		'radius': 100000,
		'client_id': 'W2A3U41LO1HEP1HIAWLYIULTXHHGUWT01PK5S30WVQMFCY34',
		'client_secret': 'FR0DLZP2RP0D05RECBLGQXYKDKG3TDG2ZEPK5MPRKIUF4SST',
		'v':20161116,
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
				
		for i in threads:
			i.start()
			print(str(self.process_count*100/self.total_pages) + '%')
			sys.stdout.write("\033[F")
		
		for i in threads:
			i.join()
			print(str(self.process_count*100/self.total_pages) + '%')
			sys.stdout.write("\033[F")
				
		self.printResults()
	


	def printResults(self):
		print 'Venues added: ' + str(self.success_venue_count)
		print 'Parsed pages: ' + str(self.success_count)
		print 'Exist venues: ' + str(self.error_venue_exist)
		print 'Can\'t connect to Page: ' + str(self.error_connection_count)
		print 'Can\'t decode JSON:' + str(self.error_decode_count)
		print 'Execution time: {:.3f}'.format(time.time() - self.start_time) + 'sec'



	def getTotalResults(self):
		r = requests.get(self.url, params=self.params).json()
		return r['response']['totalResults']



	def parseUrl(self, offset):
		params = self.params
		params['offset'] = offset * self.limit
		try:
			r = requests.get(self.url, params=params).json()
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
		except:
			category = None



		try:
			Venue(
				vid = vid,
				name = name,
				address = address,
				category = category,
				lat = lat,
				lng = lng
			).save()
			self.success_venue_count += 1
		except:
			self.error_venue_exist += 1
