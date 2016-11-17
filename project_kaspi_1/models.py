from django.contrib.gis.db import models
from django.contrib.gis import geos

class Venue(models.Model):
	vid = models.CharField(max_length=128, unique=True, blank=True, null=True)
	name = models.CharField(max_length=128, blank=True, null=True)
	address = models.CharField(max_length=128, blank=True, null=True)
	category = models.CharField(max_length=128, blank=True, null=True)

	lat = models.FloatField(blank=True, null=True)
	lng = models.FloatField(blank=True, null=True)
	point = models.PointField(blank=True, null=True)

	def __unicode__(self):
		return unicode(self.name + '->->->' +self.address)

	def save(self, *args, **options):
		if(self.lat and self.lng):
			self.point = geos.Point(self.lat, self.lng)
		return super(Venue, self).save(*args, **options)


class Tip(models.Model):
	tid = models.CharField(max_length=128, unique=True, blank=True, null=True)
	vid = models.CharField(max_length=128, blank=True, null=True)
	name = models.CharField(max_length=128, blank=True, null=True)
	text = models.TextField()