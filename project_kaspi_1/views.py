from django.shortcuts import render

from .models import Venue



def index(request):
	return render(request, 'index.html', {'data': 'something wrong'})

def search(request):
	return None

def venues(request):
	return None