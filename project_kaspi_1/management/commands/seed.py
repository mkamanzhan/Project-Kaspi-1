from django.core.management.base import BaseCommand
import requests
import sys
import time

from project_kaspi_1.management.commands._seed_venues import VenueSeeder
from project_kaspi_1.management.commands._seed_tips import TipSeeder

class Command(BaseCommand):
	

	def handle(self, *args, **options):
		print '-'*5 + ' Upload Venue ' + '-'*5
		venue_seeder = VenueSeeder()
		venue_seeder.seed()

		print '\n\n'+'-'*5 + ' Upload Tips ' + '-'*5
		tip_seeder = TipSeeder()
		tip_seeder.seed()