from django.contrib.gis.db import models
from django.contrib.gis import geos
from project_kaspi_1.es_mappings import es_mappings, es_ind_settings, model_es_indices, es_index_name
from project_kaspi_1 import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

import json
import datetime

class Venue(models.Model):
	vid = models.CharField(max_length=128, unique=True, blank=True, null=True)
	name = models.CharField(max_length=128, blank=True, null=True)
	address = models.CharField(max_length=128, blank=True, null=True)
	category = models.CharField(max_length=128, blank=True, null=True)
	tips = ArrayField(models.CharField(max_length=200), default=[])
	icon_url = models.CharField(max_length=256, blank=True, null=True)

	lat = models.FloatField(blank=True, null=True)
	lng = models.FloatField(blank=True, null=True)
	point = models.PointField(blank=True, null=True)
	
	def save(self, *args, **options):
		if(self.lat and self.lng):
			self.point = geos.Point(self.lat, self.lng)
		return super(Venue, self).save(*args, **options)

	def es_repr(self, model_name):
		data = {}
		mapping = es_mappings
		data['_id'] = self.pk
		for field_name in mapping[model_name]['properties'].keys():
			data[field_name] = self.field_es_repr(field_name, model_name)
		return data

	def field_es_repr(self, field_name, model_name):
		mapping = es_mappings
		config = mapping[model_name]['properties'][field_name]
		field_es_value = getattr(self, field_name)
		return field_es_value

	@classmethod
	def get_es_index(cls):
		return model_es_indices[cls.__name__]['index_name']

	@classmethod
	def get_es_type(cls):
		return model_es_indices[cls.__name__]['type']

	@classmethod
	def es_search(cls, term):
		es = settings.ES_CLIENT
		query = cls.gen_query(term)
		#print json.dumps(query, ensure_ascii=False)
		recs = []
		res = es.search(index=cls.get_es_index(), doc_type=cls.get_es_type(), body=query)
		if res['hits']['total'] > 0:
			print 'found %s' % res['hits']['total']
			ids = [
					c['_id'] for c in res['hits']['hits']
					]
			clauses = ' '.join([
				'WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(ids)
				])
			ordering = 'CASE %s END' % clauses
			recs = cls.objects.filter(id__in=ids).extra(select={'ordering': ordering}, order_by=('ordering',))
		return recs
	
	@classmethod
	def gen_query(cls, term):
		query = {
			"query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "should": [
                                { "multi_match": {
                                    "type": "cross_fields",
                                    "fields": ["name"],
                                    "fuzziness": "AUTO",
                                    "query": term,
                                    "boost": 10
                                } },
                                { "multi_match": {
                                    "type": "cross_fields",
                                    "fields": ["category","address"],
                                    "fuzziness": "AUTO",
                                    "query": term,
                                    "boost": 5
                                } },
                                { "multi_match": {
                                    "type": "cross_fields",
                                    "fields": ["tips"],
                                    "fuzziness": "AUTO",
                                    "query": term
                                } }
                            ]
                        }
                    }
                }
            },
            "size": 35
		}
		return json.dumps(query)


