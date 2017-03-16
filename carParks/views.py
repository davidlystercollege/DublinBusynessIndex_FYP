from __future__ import division
#from django.shortcuts import render
from django.http import HttpResponse

import xml.etree.ElementTree as et
import requests
import urllib2
from carParks.models import CP, CapacityLevel

def home(request):
    return HttpResponse("This'll be the carParks homepage")

def carParks(request):
    
    carpark_url = 'http://opendata.dublincity.ie/TrafficOpenData/CP_TR/CPDATA.xml'
    file = urllib2.urlopen(carpark_url)
    #response = urllib.request.urlopen(carpark_url)

    def createCarPark(request, namearg):
        cp = CP()
        cp.name = namearg
        cp.save()
        return
    
    def createCPCapacityLevel(request, CP, avSpaces, fullness):
        cl = CapacityLevel(carParkObj = CP, availableSpaces = avSpaces, percentFull = fullness)
        cl.name = CP.name
        cl.save()
        return
    
    def getCapacityDetails():
        ans = ""
        fullness=0
        
        '''
        tree = et.parse(file)
        root = tree.getroot()
        '''
        
        root= et.fromstring(file)
        
        spaces=0
        for child in root:
            for children in child:
                    
                tempname = children.get('name')
                spaces = children.get('spaces')            
                    
                cpRef = CP.objects.all().get(name = tempname)
                
                #null data check
                if(spaces == " "):
                    spaces=cpRef.capacity
                    
                if(spaces=="FULL"):
                    spaces = 0
                
                fullness = ( ( (int(cpRef.capacity) - int(spaces)) / cpRef.capacity) * 100)
                    
                ans = ans + str(tempname) + ' : ' + str(spaces) +  " : fullness : " + str(fullness) + "<br><br/>"                
                    
                if(fullness > 100 or fullness < 100):
                    fullness = 100  # negative values have shown up where the amount of GIVEN available spaces
                                    # is greater than the actual amount of spaces in the CP
                          
                createCPCapacityLevel(request, cpRef, spaces, fullness)    
        
        return ans
    
    def getBusyness_Avg():
        busyness = 0.0
        fullness=0
        tree = et.parse(file)
        root = tree.getroot()
        spaces=0
        
        x = ''
        
        tempAvg = 40.2856
        
        for child in root:
            for children in child:
                    
                tempname = children.get('name')
                spaces = children.get('spaces')            
                    
                cpRef = CP.objects.all().get(name = tempname)
                
                #null data check
                if(spaces == " "):
                    spaces=cpRef.capacity
                    
                if(spaces=="FULL"):
                    spaces = 0
                
                fullness = ( ( (int(cpRef.capacity) - int(spaces)) / cpRef.capacity) * 100)
                    
                busyness = busyness + (float(fullness) - tempAvg)
                  
                #x = x + str(busyness) + ': ' + str(fullness) + ': ' + str(spaces) + '<br><br/>'    
                #ans = ans + str(tempname) + ' : ' + str(spaces) +  " : fullness : " + str(fullness) + "<br><br/>"                
                    
                createCPCapacityLevel(request, cpRef, spaces, fullness)    
        
        return busyness
    
    def getBusyness():
        busyness = 0.0
        fullness=0
        tree = et.parse(file)
        root = tree.getroot()
        spaces=0
        count=1
        ans=''
        for child in root:
            for children in child:
                    
                tempname = children.get('name')
                spaces = children.get('spaces')            
                    
                cpRef = CP.objects.all().get(name = tempname)
                
                if(cpRef.name == "THOMASST"):
                    continue    # not recording data
                
                #null data check
                if(spaces == " "):
                    spaces=cpRef.capacity
                    
                if(spaces=="FULL"):
                    spaces = 0
                
            
                
                fullness = ( ( (int(cpRef.capacity) - int(spaces)) / cpRef.capacity) * 100)
                
                if(fullness > 100 or fullness < 0):
                    fullness = 100
                    
                busyness = busyness + float(fullness)
                  
                #x = x + str(busyness) + ': ' + str(fullness) + ': ' + str(spaces) + '<br><br/>'    
                #ans = ans + str(tempname) + ' : ' + str(spaces) +  " : fullness : " + str(fullness) + "<br><br/>"                
                
                ans=ans + cpRef.name + ": " + str(fullness) + " - (Spc, Cap): " + str(spaces) + ", " + str(cpRef.capacity) + "<br><br/>"    
                createCPCapacityLevel(request, cpRef, spaces, fullness)  
                count=count+1  
                  
        busyness = (busyness/count-1)
        return busyness
    
    #return HttpResponse(getCapacityDetails())
    #return HttpResponse(getBusyness())
    return getBusyness()

def tests(request):
    carpark_url = 'http://opendata.dublincity.ie/TrafficOpenData/CP_TR/CPDATA.xml'
    file = urllib2.urlopen(carpark_url)
    
    def getBusyness2():
        busyness = 0.0
        fullness=0
        tree = et.parse(file)
        root = tree.getroot()
        spaces=0
        count=1
        ans=''
        for child in root:
            for children in child:
                    
                tempname = children.get('name')
                spaces = children.get('spaces')            
                    
                cpRef = CP.objects.all().get(name = tempname)
                
                if(cpRef.name == "THOMASST"):
                    continue    # not recording data
                
                #null data check
                if(spaces == " "):
                    spaces=cpRef.capacity
                    
                if(spaces=="FULL"):
                    spaces = 0
                
            
                
                fullness = ( ( (int(cpRef.capacity) - int(spaces)) / cpRef.capacity) * 100)
                
                if(fullness > 100 or fullness < 0):
                    fullness = 100
                    
                busyness = busyness + float(fullness)
                  
                #x = x + str(busyness) + ': ' + str(fullness) + ': ' + str(spaces) + '<br><br/>'    
                #ans = ans + str(tempname) + ' : ' + str(spaces) +  " : fullness : " + str(fullness) + "<br><br/>"                
                
                ans=ans + str(cpRef.name) + ": " + str(fullness) + " - (Spc, Cap): " + str(spaces) + ", " + str(cpRef.capacity) + "<br><br/>"
                ans=ans + "Busyness: " +str(busyness) + "<br>"
                #createCPCapacityLevel(request, cpRef, spaces, fullness)  
                count=count+1  
                  
        busyness = (busyness/count-1)
        return ans
    
    #return HttpResponse(getCapacityDetails())
    return HttpResponse(getBusyness2())