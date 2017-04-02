from __future__ import division
from django.http import HttpResponse
import json
import requests
from noiseLevels.models import Meter, Reading

def home(request):
    return HttpResponse("This'll be the Noise Level homepage")

def noiseLevels(request):
    
    def createMeter(request, namearg):
        # Unlikely to be needed again
        mt = Meter()
        mt.name = namearg
        mt.save()
        return
    
    def createReading(request, Meter, namearg, aleqarg, giventime, givendate):
        rd = Reading.objects.create(rdObj = Meter, name = Meter.name, aleq = aleqarg, timeRecorded = giventime, dateRecorded = givendate)
        rd.save()
        return
    
    def getAllLocations():  
        ans =''  
        allLocationsAPI = 'http://dublincitynoise.sonitussystems.com/applications/api/dublinnoisedata.php?returnLocationStrings=true&location=all'
        allLocationsReq = requests.get(allLocationsAPI)
        
        decoded_content = allLocationsReq.content.decode('utf-8')
        allLocations = json.loads(decoded_content)
        
        for i in range(0,14):
            ans = ans + str(allLocations[i]) + '<br><br/>'
        return ans
      
    def getSpecificLocationData():
        ans = ''
        
        ''' 1-13* '''
        for index in range(1,13):
            locationReqAPI = 'http://dublincitynoise.sonitussystems.com/applications/api/dublinnoisedata.php?location='+str(index)
            locationReq = requests.get(locationReqAPI)
            
            decoded_content = locationReq.content.decode('utf-8')
            locationStr = json.loads(decoded_content)
            
            ans = ans + str(Meter.objects.get(id=index)) + ' - '
            ans = ans + (str(index) + ": " + locationStr['dates'][-1] + ": " + locationStr['times'][-1] + ": " + locationStr['aleq'][-1]) + '<br><br/>'
            
            rdRef = Meter.objects.get(id = index)
            createReading(request, rdRef, rdRef.name, locationStr['aleq'][-1], locationStr['times'][-1], locationStr['dates'][-1])
    
        return ans
    
    def getNoiseBusyness_Avg():
        ans = ''
        addx = ''
        busyness = 0.0
        
        tempAverage = 55.933
        
        ''' 1-13* '''
        for index in range(1,13):
            locationReqAPI = 'http://dublincitynoise.sonitussystems.com/applications/api/dublinnoisedata.php?location='+str(index)
            locationReq = requests.get(locationReqAPI)
            
            decoded_content = locationReq.content.decode('utf-8')
            locationStr = json.loads(decoded_content)
            
            aleq = locationStr['aleq'][-1]
            
            ans = ans + str(Meter.objects.get(id=index)) + ' - '
            ans = ans + (str(index) + ": " + locationStr['dates'][-1] + ": " + locationStr['times'][-1] + ": " + aleq) + '<br><br/>'
            
            rdRef = Meter.objects.get(id = index)
            createReading(request, rdRef, rdRef.name, aleq, locationStr['times'][-1], locationStr['dates'][-1])
    
            busyness = busyness + (float(aleq) - tempAverage)
            #addx = addx + str(index) + ': ' + str(busyness) + ': ' + str(float(aleq) - tempAverage) + ': ' + str((locationStr['aleq'][-1])) + '<br><br/>'
            
        return busyness
    
    def getNoiseBusyness():
        ans = ''
        busyness = 0.0
        count=0
        
        fail = 0;
        ''' 1-13* '''
        if fail == 0:
            for index in range(1,13): 
                locationReqAPI = 'http://dublincitynoise.sonitussystems.com/applications/api/dublinnoisedata.php?location='+str(index)
                try:
                    locationReq = requests.get(locationReqAPI)
                    decoded_content = locationReq.content.decode('utf-8')
                    locationStr = json.loads(decoded_content)
                    
                    aleq = locationStr['aleq'][-1]
                    
                    ans = ans + str(Meter.objects.get(id=index)) + ' - '
                    ans = ans + (str(index) + ": " + locationStr['dates'][-1] + ": " + locationStr['times'][-1] + ": " + aleq) + '<br><br/>'
                    
                    rdRef = Meter.objects.get(id = index)
                    createReading(request, rdRef, rdRef.name, aleq, locationStr['times'][-1], locationStr['dates'][-1])
            
                    busyness = busyness + float(aleq)
                    #addx = addx + str(index) + ': ' + str(busyness) + ': ' + str(float(aleq) - tempAverage) + ': ' + str((locationStr['aleq'][-1])) + '<br><br/>'
                    count=count+1
                except:
                    fail = 1
        else:
            busyness=40
            count=1    
        '''
        seeing as range is 20<aleq>70, (length 50), if we take 20 off the 
        average current reading, it'll be in the range of 0<aleq>50, so then 
        mulitplying that by 2 gives us the busyness factor in 0<aleq>100
        '''    
        tst = (busyness/count)    
        busyness = ( ( (busyness/count) -20 ) *2 )
        return busyness
    
    return getNoiseBusyness()
    #return HttpResponse(getNoiseBusyness())

'''

*: 13&14: DOLPHIN & MELLOWS are not providing correct data through API

'''