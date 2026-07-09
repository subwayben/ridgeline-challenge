from django.shortcuts import render

def home(request):
    return render(request, "dashboard/home.html")

from django.http import HttpResponse
def city(request, city_name):
    return HttpResponse(f"You selected: {city_name}")
# Create your views here.
