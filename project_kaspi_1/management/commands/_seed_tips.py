import requests
import threading
import math
import time

from project_kaspi_1.models import Venue, Tip
from project_kaspi_1.management.commands._fsq_settings import fsq_settings

class TipSeeder:
	limit = 100

	url = fsq_settings['tip']['url']
	params = {
		'sort': fsq_settings['tip']['sort'],
		'client_id': fsq_settings['client_id'],
		'client_secret': fsq_settings['client_secret'],
		'v':fsq_settings['v'],
	}
	
	threads = []

	#Tip's Statistics
	success_tips = 0
	success_tips_pages = 0
	error_tips_connection = 0
	error_tips_decode = 0
	error_tips_exist = 0


	start_time = 0



	def seed(self):
		self.start_time = time.time()

		Tip.objects.all().delete()
		venues = Venue.objects.all()

		pages_threads = []

		if(len(venues) == 0):
			print 'No venues detected\nFirstly upload venues'
		for venue in venues:
			pages_threads.append(threading.Thread(target=self.parseVenue, args=(venue.vid,)))

		self.runThreads(pages_threads)
		self.runThreads(self.threads)
		self.printResults()



	def printResults(self):
		print 'Tips added: ' + str(self.success_tips)
		print 'Parsed pages: ' + str(self.success_tips_pages)
		print 'Exist tips: ' + str(self.error_tips_exist)
		print 'Can\'t connect to Page: ' + str(self.error_tips_connection)
		print 'Can\'t decode JSON:' + str(self.error_tips_decode)
		print 'Execution time: {:.3f}'.format(time.time() - self.start_time) + 'sec'



	def runThreads(self, threads, thread_limit=20):
		length = len(threads)
		for i in range(length):
			if(i%thread_limit==0):
				for thread in threads[i-thread_limit:i]:
					thread.start()
				for thread in threads[i-thread_limit:i]:
					thread.join()
					
			elif(i == length-1):
				for thread in threads[(i/thread_limit)*thread_limit:i+1]:
					thread.start()
				for thread in threads[(i/thread_limit)*thread_limit:i+1]:
					thread.join()



	def parseVenue(self, vid):
		total_result = self.getTotalResults(vid)
		total_pages = int(math.ceil(total_result / self.limit)) + 1
		for i in range(total_pages):
			self.threads.append(threading.Thread(target=self.parseUrl, args=(vid, i * self.limit,)))
	
		

	def getTotalResults(self,vid):
		try:
			r = requests.get(self.url.format(vid), params=self.params).json()
			if(r['meta']['code'] == 200):
				return r['response']['tips']['count']
			else:
				return 1
		except requests.exceptions.ConnectionError:
			self.error_tips_connection += 1
			return 1
		
		except ValueError:
			self.error_tips_decode += 1
			return 1



	def parseUrl(self, vid, page):
		params = self.params
		params['offset'] = page
		try:
			r = requests.get(self.url.format(vid), params=self.params).json()
			if(r['meta']['code'] == 200):
				for item in r['response']['tips']['items']:
					self.saveTip(item, vid)
				self.success_tips_pages += 1
			else:
				self.error_tips_decode += 1
		except requests.exceptions.ConnectionError:
			self.error_tips_connection += 1
		except ValueError:
			self.error_tips_decode += 1



	def saveTip(self, item, vid):
		tid = item['id']
		text = item['text']
		name = item['user']['firstName']
		
		try:
			Tip(
				tid = tid,
				vid = vid,
				name = name,
				text = text
			).save()
			self.success_tips += 1
		except:
			self.error_tips_exist += 1