from rest_framework import serializers
from . import models

class VenueSerializer(serializers.Serializer):
	class Meta:
		model = Venue