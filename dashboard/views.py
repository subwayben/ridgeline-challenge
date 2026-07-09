from django.shortcuts import render
from .data_loader import get_chart_data

CITY_INFO = {
    "los_angeles": {
        "display_name": "Los Angeles, CA",
        "cbsa_name": "Los Angeles-Long Beach-Anaheim, CA",
    },
    "san_diego": {
        "display_name": "San Diego, CA",
        "cbsa_name": "San Diego-Chula Vista-Carlsbad, CA",
    },
    "new_york": {
        "display_name": "New York City, NY",
        "cbsa_name": "New York-Newark-Jersey City, NY-NJ-PA",
    },
}

def home(request):
    return render(request, "dashboard/home.html")

def city(request, city_name):
    city_info = CITY_INFO[city_name]
    chart_data = get_chart_data(city_info["cbsa_name"])

    context = {
        "city_name": city_info["display_name"],
        "dates": chart_data["dates"],
        "values": chart_data["values"],
    }

    return render(request, "dashboard/city.html", context)