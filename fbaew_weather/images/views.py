from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def images(request):
	return HttpResponse("Hello world!")

def yearly_radar(request,year):
    return HttpResponse("We don't yet support yearly radar images.")

def daily_radar(request,year,month,day):
    response = "Radar images for {}/{}/{}".format(year,month,day)
    return HttpResponse(response)

