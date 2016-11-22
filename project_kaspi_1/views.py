from django.shortcuts import render

from .models import Venue
from .serializers import VenueGeoSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def index(request):
	return render(request, 'index.html')

class SearchView(APIView):
	renderer_classes = (JSONRenderer,)

	def get(self, request):
		term = request.GET.get('text')
		result_of_search_venue = Venue.es_search(term)
		venue_serializer = VenueGeoSerializer(result_of_search_venue, many = True)
		data = venue_serializer.data
		return Response({'data': data})
