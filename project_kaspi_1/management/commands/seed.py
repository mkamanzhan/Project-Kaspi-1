# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import requests
import sys
import time
from elasticsearch.client import IndicesClient
from django.conf import settings
from project_kaspi_1.management.commands._seed_venues import VenueSeeder
from project_kaspi_1.management.commands._seed_tips import TipSeeder
from project_kaspi_1.es_mappings import es_mappings, es_ind_settings, model_es_indices, es_index_name, es_models
from elasticsearch.helpers import bulk
from project_kaspi_1.models import Venue

class Command(BaseCommand):
	

	def handle(self, *args, **options):
		start_time = time.time()
		print '-'*5 + ' Upload Venues ' + '-'*5
		venue_seeder = VenueSeeder()
		venue_seeder.seed()

		print '\n\n'+'-'*5 + ' Upload Tips ' + '-'*5
		tip_seeder = TipSeeder()
		tip_seeder.seed()
		
		self.recreate_index()
		self.push_db_to_index()

		print '\nTotal execution time: {:.3f}'.format(time.time() - start_time) + 'sec'

	def recreate_index(self):
		indices_client = IndicesClient(client = settings.ES_CLIENT) 
		index_name = es_index_name
		if indices_client.exists(index_name):
			indices_client.delete(index = index_name)
		indices_client.create(index = index_name, body = es_ind_settings)
		for model_name in es_models:
			indices_client.put_mapping(
				doc_type=model_es_indices[model_name]['type'],
				body=es_mappings[model_name],
				index=es_index_name
			)

	def push_db_to_index(self):
		data = [
			self.convert_for_bulk(venue, 'create') for venue in Venue.objects.all()]
		bulk(client=settings.ES_CLIENT, actions=data, stats_only=True)
		

	def convert_for_bulk(self, django_object, action = None):
		data = django_object.es_repr(django_object.__class__.__name__)
		metadata = {
			'_op_type' : action,
			'_index' : model_es_indices[django_object.__class__.__name__]['index_name'],
			'_type' : model_es_indices[django_object.__class__.__name__]['type']
		} 
		data.update(**metadata)
		return data




