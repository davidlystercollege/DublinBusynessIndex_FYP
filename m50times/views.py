from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse

import json
from pprint import pprint
import requests
from m50times.models import Route, Recording

def home(request):
    return HttpResponse("This'll be the m50 homepage")

def m50times(request):
    
    fail = 0;
    
    m50_url = 'http://dataproxy.mtcc.ie/v1.5/api/traveltimes.json'
    try:
        m50data = requests.get(m50_url)
    except:
        fail = 1
        
    routes = ['J17 Shankill -> J16 Cherrywood','J16 Cherrywood -> J15 Ballyogan',
              'J15 Ballyogan -> J13 Balinteer','J13 Balinteer -> J12 Scholarstown',
              'J12 Scholarstown -> J11 Balrathory','J11 Balrathory -> J9 Red Cow',
              'J9 Red Cow -> J7 Palmerstown','J7 Palmerstown -> Blanchardstown',
              'Blanchardstown -> J5 Finglas','J5 Finglas -> J3 M1/N32/DPT',
              'J17 Shankill -> J3 M1/N32/DPT']
    
    def isInteger(v):
        if(isinstance(v, int) == True):
            return True
        else:
            False      
    
    def createRoute(request, routename, routefrom, routeto):
        # probably will not need to be used again
        ru = Route()
        ru.name = routename
        ru.rfrom = routefrom
        ru.rto = routeto
        ru.save()
        return   
      
    def createRecording(request, Route, time):  
        rec = Recording.objects.create(ruObj = Route, name = Route.name, traveltime = time)
        rec.save()
        return
    
    '''
    def getCurrTT():
        
                
        decoded_content = m50data.content.decode('utf-8')
        z = json.loads(decoded_content)
            
        i=0
        data = ''
        while(i < 11):
            
            if(i < len(z["M50_northBound"]['data'])):
                
                routename = str(z["M50_northBound"]['data'][i]["from_name"] + ' -> ' + z["M50_northBound"]['data'][i]['to_name'])
                routenum = routes.index(routename)
                routetime = z["M50_northBound"]['data'][i]['current_travel_time']
                
                data = data + 'Route ' + str(routenum) + ': ' + str(routename + ': ' + str(routetime)) + '<br><br/>'
                 
                ruRef = Route.objects.get(name = routename)
                createRecording(request, ruRef, routetime)
                        
                i=i+1
            else:    
                data = data + 'Fail at index '+str(i) + ' where data size = '+str(len(z["M50_northBound"]['data'])) + '<br><br/>'
                i=i+1
               
        return data
        
    def getCurrTTBusyness_Avg():
        busyness = 0.0
        busyness2 = 0.0
        
        decoded_content = m50data.content.decode('utf-8')
        z = json.loads(decoded_content)
            
        i=0
        data = ''
        tempAverage = 178.0655
        tempAverage2 = 1609.894
        
        ans =''
        
        while(i < 11):
            
            if(i < len(z["M50_northBound"]['data'])):
                
                routename = str(z["M50_northBound"]['data'][i]["from_name"] + ' -> ' + z["M50_northBound"]['data'][i]['to_name'])
                routenum = routes.index(routename)
                routetime = z["M50_northBound"]['data'][i]['current_travel_time']
                
                data = data + 'Route ' + str(routenum) + ': ' + str(routename + ': ' + str(routetime)) + '<br><br/>'
                
                if(routename != 'J17 Shankill -> J3 M1/N32/DPT'):
                    busyness = busyness + (float(routetime) - tempAverage)
                else:
                    busyness2 = busyness2 + (float(routetime) - tempAverage2)
                     
                ruRef = Route.objects.get(name = routename)
                createRecording(request, ruRef, routetime)
                
                ans = ans + str(routetime) + ': ' + str(busyness) + ': ' + str(busyness2) + '<br><br/>'
                        
                i=i+1
            else:    
                data = data + 'Fail at index '+str(i) + ' where data size = '+str(len(z["M50_northBound"]['data'])) + '<br><br/>'
                i=i+1
               
        #return str(busyness) + ': ' + str(busyness2)   
        #return ans
        return busyness
    
    '''
    def getCurrTTBusyness():
        busyness = 0.0
        
        return m50data
    
    #return HttpResponse(getCurrTTBusyness())
    return getCurrTTBusyness()