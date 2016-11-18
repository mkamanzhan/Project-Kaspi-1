from django.shortcuts import render

from .models import Venue
from .serializers import VenueGeoSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def index(request):
	return render(request, 'index.html', {'data': 'something wrong'})

def search(request):
	return None

def venues(request):
	return None

class VenueView(APIView):
	renderer_classes = (JSONRenderer,)

	def get(self, request):
		venues = Venue.objects.all()
		venue_serializer = VenueGeoSerializer(venues, many=True)
		data = venue_serializer.data
		return Response({'data': data})