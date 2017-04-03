from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse

import json
from pprint import pprint
import requests
from m50times.models import Route, Recording
from docutils.parsers import null

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
        
        if(fail == 0):
            decoded_content = m50data.content.decode('utf-8')
            z = json.loads(decoded_content)
                
            i=0
            data = ''
            
            rangeMaxs = [61,89,200,900,318,900,537,190,240,240,0]   # last 0 is placeholder for overall/last route
            rangeSizes = [2,10,100,640,260,800,400,75,130,40,1]
            
            
            while(i < 11):
                    
                busy_nw=0.0
                busy=0.0
                
                if(i < len(z["M50_northBound"]['data'])):
                    if z["M50_northBound"]['data'] == []:
                        break
                    
                    if z["M50_northBound"]['data'] == null:
                        break
                    routename = str(z["M50_northBound"]['data'][i]["from_name"] + ' -> ' + z["M50_northBound"]['data'][i]["to_name"])
                    routenum = routes.index(routename)
                    routetime = z["M50_northBound"]['data'][i]["current_travel_time"]
                
                    rngeMax=rangeMaxs[routenum]
                    rngeSize=rangeSizes[routenum]
                    
                    #data = data + 'Route ' + str(routenum) + ': ' + str(routename + ': ' + str(routetime)) + '<br><br/>'
                    
                    '''if(routename != 'J17 Shankill -> J3 M1/N32/DPT'):
                        continue
                    
                    '''
                    #data = data + str(z["M50_northBound"]['data'][i]) + "<br><br/>"
                    if(routenum!=10):
                        
                        if(routetime>rngeMax):
                            busy_nw = 1
                        else:
                            rngeLocation = rngeSize - (rngeMax - routetime)
                            busy_nw = (rngeLocation/rngeSize)
                              
                            rangeWeight = (rngeSize/2457)
                            # int value above.......^^^ is sum of all range sizes
                            
                        busy = (busy_nw * rangeWeight)                
                        
                        busyness = busyness + busy                
                        
                        data = data + "r(w,s,l) = " + str(rngeMax) + ", " + str(rngeSize) + ", " + str(rngeLocation)
                        data = data + 'Route ' + str(routenum) + ': ' + str(routename + ': ' + str(routetime)) + " - busynw = " +str(busy_nw)+ " - B: " + str(busy*100) + '<br><br/>'
                        
                        #data = data + "size, max, num := " + str(rngeSize) + ", "  + str(rngeMax) + ", " + str(rangeWeight) + "<br><br/>"
                        
                    '''
                    1: top =      rng(size) - ( rng(max) - routeTime )
                    2: busyness = top / rng(size)                
                    '''
                    
                    ruRef = Route.objects.get(name = routename)
                    createRecording(request, ruRef, routetime)
                    
                    #ans = ans + str(routetime) + ': ' + str(busyness) + ': ' + str(busyness2) + '<br><br/>'
                            
                    i=i+1
                else:   
                    data = data + 'Fail at index '+str(i) + ' where data size = '+str(len(z["M50_northBound"]['data'])) + '<br><br/>'
                    #i=i+1
                   
            #return str(busyness) + ': ' + str(busyness2)   
            #return ans
            busyness = 10.34342113
            data=data + "Busyness = " +str(busyness)
            busyness=(busyness*100)
            busyness = 10.34342113
        else:
            busyness = 10.34342113  # hard code in average for when dataset is not live
                                    # this will be very slow hours so the average is halved
        return busyness
    
    #return HttpResponse(getCurrTTBusyness())
    return getCurrTTBusyness()