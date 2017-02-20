from __future__ import division
#from django.shortcuts import render
from django.http import HttpResponse

from dublinBikes.models import BikeStation, Availability
import requests
import json

def home(request):
    return HttpResponse("This'll be the Dublin Bikes homepage")

def dubBikes(request):
    
    apiKey = "597b20fdf17e60114fc2dabd44108903a1424fcc"
    
    stations = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=597b20fdf17e60114fc2dabd44108903a1424fcc")
    #add '/x' before '?' to get station number 'x'
    
    def createBikeStation(request, namearg, tbs):
        bs = BikeStation()
        bs.name = namearg
        bs.totalBikeStands = tbs
        bs.save()
        return
    
    # this is the main function recording availabilites of bikes at stations
    def createBSInstance(request, BikeStation, avBikes, avStands, avail):
        av = Availability.objects.create(bsObj = BikeStation, availableBikes = avBikes, availableStands = avStands, percentFull = avail)
        av.name = BikeStation.name
        av.save()
        return
    
    def allStations():   
        ans = "*where available_bikes + available_bike_stands = (total)bike_stands" 
        decoded_content = stations.content.decode('utf-8')
        jsonStation = json.loads(decoded_content)
        
        count=1
        
        for e in jsonStation:
            
            pcFull = ( ( e['available_bikes']/e['bike_stands'] ) * 100 )            
            
            ans = ans + "<br><br/>" + ( str(count) + ': ' + e['name'] + ' : ' + str(e['available_bikes']) + '+' + str(e['available_bike_stands']) + ' = '
                                        + str(e['bike_stands']))
            
            bsRef = BikeStation.objects.get(name = e['name'])
            
            if(pcFull > bsRef.totalBikeStands):
                pcFull = 100
            createBSInstance(request, bsRef, e['available_bikes'], e['available_bike_stands'], pcFull)
            
            count = count + 1
            
        return ans
    
    def getBusyness_Avg():   
        busyness = 0.0
        decoded_content = stations.content.decode('utf-8')
        jsonStation = json.loads(decoded_content)
        
        count=1
        
        tempAvg = 40.852
        
        for e in jsonStation:
            
            pcFull = ( ( e['available_bikes']/e['bike_stands'] ) * 100 )            
            
            '''ans = ans + "<br><br/>" + ( str(count) + ': ' + e['name'] + ' : ' + str(e['available_bikes']) + '+' + str(e['available_bike_stands']) + ' = '
                                        + str(e['bike_stands']))'''
            
            busyness = busyness + (float(pcFull) - tempAvg)
            bsRef = BikeStation.objects.get(name = e['name'])
            if(pcFull > bsRef.totalBikeStands):
                pcFull = 100
            createBSInstance(request, bsRef, e['available_bikes'], e['available_bike_stands'], pcFull)
            
            count = count + 1
            
        return busyness
    
    def getBusyness():   
        busyness = 0.0
        decoded_content = stations.content.decode('utf-8')
        jsonStation = json.loads(decoded_content)
        
        count=0
        for e in jsonStation:
            
            pcFull = ( ( e['available_bikes']/e['bike_stands'] ) * 100 )            
            
            '''ans = ans + "<br><br/>" + ( str(count) + ': ' + e['name'] + ' : ' + str(e['available_bikes']) + '+' + str(e['available_bike_stands']) + ' = '
                                        + str(e['bike_stands']))'''
            
            bsRef = BikeStation.objects.get(name = e['name'])
            
            if(pcFull > bsRef.totalBikeStands):
                pcFull = 100
            busyness = busyness + pcFull            
            
            createBSInstance(request, bsRef, e['available_bikes'], e['available_bike_stands'], pcFull)
            
            count = count + 1
        
        busyness = (busyness/count)    
        return busyness
    #return HttpResponse(allStations())
    #return getBusyness() # for when the main calls the function
    return getBusyness() # for the function called implicitly