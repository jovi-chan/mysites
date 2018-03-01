from django.shortcuts import render
from zeep import Client
import requests
import json
from django.http.response import HttpResponse

id = '[FlightStat-id]'
key = '[FlightStat-key]'

def countries():
    countryUrl = "https://restcountries.eu/rest/v2/all"
    response = requests.get(countryUrl)
    result = json.loads(response.text)
    countryList = []
    for country in result:
        countryNameCode = {'name': country['name'], 'code' :country['alpha2Code']}
        countryList.append(countryNameCode)
    return countryList

def airport(request):
    countryList = countries()
    if request.method != 'POST':
        return render(request, "airport.html", {'country': countryList})
    else:
        try:
            airportUrl = "https://api.flightstats.com/flex/airports/soap/v1/airportsService?wsdl"
            client = Client(airportUrl)
            countryInput = request.POST['countryInput']
            response = client.service.countryCode_airports(appId = id, appKey = key, countryCode = countryInput)
        except:
            return HttpResponse(json.dumps({'action': 'error', 'airportResult': "Error in reading airport API."}))
        
        airportList = []
        for airportData in response: 
            if (airportData["active"]) and (airportData["classification"] <= 2) :
                airportDetail = {
                    'name': airportData["name"],
                    'city': airportData["city"],
                    'latitude': airportData["latitude"],
                    'longitude': airportData["longitude"],
                    'temperature': weather(airportData["fs"]),
                    'localtime': airportData["localTime"],
                    }
                airportList.append(airportDetail)
    return HttpResponse(json.dumps({'action': 'success', 'airportResult': airportList}))


def weather(fs):
    try: 
        weatherUrl = "https://api.flightstats.com/flex/weather/rest/v1/json/metar/"+fs+"?appId="+id+"&appKey="+key
        responseW = requests.get(weatherUrl)
        weather = json.loads(responseW.text)
        temp = weather["metar"]["temperatureCelsius"]
    except: 
        return "No result"
    return temp
    