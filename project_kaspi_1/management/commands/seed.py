from django.core.management.base import BaseCommand
import requests
import math
import threading
import sys

from project_kaspi_1.models import Venue

class Command(BaseCommand):
	url = 'https://api.foursquare.com/v2/venues/explore'
	params = {
		'll': '43.2551,76.9126',
		'limit': 100,
		'radius': 100000,
		'client_id': 'W2A3U41LO1HEP1HIAWLYIULTXHHGUWT01PK5S30WVQMFCY34',
		'client_secret': 'FR0DLZP2RP0D05RECBLGQXYKDKG3TDG2ZEPK5MPRKIUF4SST',
		'v':20161115,
	}

	total_pages = 0

	process_count = 0

	success_count = 0
	success_venue_count = 0
	error_connection_count = 0
	error_decode_count = 0
	


	def handle(self, *args, **options):
		Venue.objects.all().delete()
		threads = []
		k = 0
		self.total_pages = self.getOffsetMax()
		while(k != self.total_pages):
			threads.append(threading.Thread(target=self.parseUrl, args=(k,)))
			k += 1
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
		print 'Parsed Pages: ' + str(self.success_count)
		print 'Can\'t connect to Page: ' + str(self.error_connection_count)
		print 'Can\'t decode JSON:' + str(self.error_decode_count)



	def getOffsetMax(self):
		r = requests.get(self.url, params=self.params).json()
		return r['response']['totalResults'] - 1



	def parseUrl(self, offset):
		params = self.params
		params['offset'] = offset
		try:
			r = requests.get(self.url, params=params).json()
			if(r['meta']['code'] == 200 and len(r['response']['groups'][0]['items'])!=0):
				for item in r['response']['groups'][0]['items']:
					self.saveVenue(item)
					self.success_venue_count += 1
			self.success_count += 1
		except requests.exceptions.ConnectionError as e:
			self.error_connection_count += 1
		except ValueError:
			self.error_decode_count += 1
		self.process_count += 1



	def saveVenue(self,item):
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

		Venue(
			name = name,
			address = address,
			category = category,
			lat = lat,
			lng = lng
			).save()