from __future__ import division

from django.shortcuts import render
from django.http import HttpResponse

from dublinBikes.models import BikeStation, Availability
from carParks.models import CP, CapacityLevel
from m50times.models import Route, Recording
from noiseLevels.models import Meter, Reading
from main.models import DatasetObject, BusynessSub, BusynessIndex
from django.utils import timezone
from django.template import Context, loader

import datetime
import noiseLevels.views
import m50times.views
import dublinBikes.views
import carParks.views

def home(request):
    
    ########### Donut Data ################################
    bikeSubs = BusynessSub.objects.filter(name = "DublinBikes")
    cpSubs = BusynessSub.objects.filter(name = "CarPark")
    m50Subs = BusynessSub.objects.filter(name = "M50")
    noiseSubs = BusynessSub.objects.filter(name = "NoiseLevel")
    
    bikeVal = bikeSubs.last().busynessFactor
    cpVal = cpSubs.last().busynessFactor
    m50Val = m50Subs.last().busynessFactor
    nseVal = noiseSubs.last().busynessFactor
    
    dat = [cpVal, m50Val, bikeVal, nseVal] 
    #########################################################
    
    ########### Busyness Index #####################
    bizness = BusynessIndex.objects.last().busyness#
    ################################################
    
    ########### Line Graph 1 Data #####################
    bizys1 = []
    times1 = []
    sze = len(BusynessIndex.objects.all())
    
    for i in range(12):
        tempBiz = BusynessIndex.objects.get(id = (sze-i))
        bizys1.append(tempBiz.busyness)
        
        #tmptym = (tempBiz.dateTaken).time()
        tmptym = datetime.datetime.strptime(tempBiz.dateTaken, "%m/%j/%y %H:%M").time()
        #tmptym = ((tempBiz.dateTaken) - datetime(1970, 1, 1)).total_seconds() 
        
        
        times1.append(tmptym)
    ################################################
    
    ########### Line Graph 2 Data #####################
    ################################################
    
    ########### Bar Chart Data #####################
    ################################################
    
    
    ### Pass Required Data to our Context ##########
    context = {
        "busyIndNow": bizness,
        "donutData": dat,
        "line1bizs" : bizys1,
        "line1times" : times1,
    }
    
    ## render html page on request with respect to context ##
    return render(request, 'myDash.html', context)

def testing(request):
    
    def createBusynessSub(request, DatasetObject, busynessArg):
        bzSub = BusynessSub.objects.create(dataObj = DatasetObject, busynessFactor = busynessArg)
        bzSub.name = bzSub.dataObj.name
        bzSub.save()
        return
    
    def createBusynessIndex(request, busynessInd):
        busy = BusynessIndex.objects.create(busyness = busynessInd)
        busy.save()
        return
    
    def getDatasetObj(nameArg):
        return DatasetObject.objects.get(name = nameArg)
    
    def getBikes():
        i=0
        subtotal=0
        dso = getDatasetObj('DublinBikes')
        
        data = ''
        for bs in BikeStation.objects.all():
            tempBS = Availability.objects.all().filter(name = bs.name)
            
            for tbs in tempBS:
                data = data + str(i) + ': ' + tbs.name + ': ' + str(tbs.percentFull) + '<br><br/>'
                subtotal = subtotal + tbs.percentFull
                i=i+1 
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average)   
        return data
    
    def getCPs():
        i=0
        subtotal=0
        dso = getDatasetObj('CarPark')
        
        data = ''
        for cp in CP.objects.all():
            tempCP = CapacityLevel.objects.all().filter(name = cp.name)
            
            for tcp in tempCP:
                # THOMASST has recorded only 0 values so I will exlude it for now
                if(tcp.name != 'THOMASST'):
                    data = data + tcp.name + ': ' + str(tcp.percentFull) + '<br><br/>'
                    subtotal = subtotal + tcp.percentFull
                    i=i+1
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average) 
        return data
    
    def getNoiseMeters():
        i=0
        subtotal=0
        dso = getDatasetObj('NoiseLevel')
        
        ans=''
        data = Reading.objects.all()
        allNoises = []
        for noise in data:
            allNoises.append(noise.aleq)
        
        '''for mt in Meter.objects.all():
            tempmt = Reading.objects.all().filter(name = mt.name)
            
            for tmt in tempmt:
                data = data + tmt.name + ': ' + str(tmt.aleq) + '<br><br/>'
                subtotal = subtotal + tmt.aleq
                i=i+1
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average)'''
           
        ans = ans + str(max(allNoises)) + " <- Max, Min -> " + str(min(allNoises))     
        return ans
    
    def getM50s():
        subRouteTotal=0
        fullRouteTotal=0
        dso = getDatasetObj('M50')
        
        count=0
        
        rangeMaxs = [61,89,173,602,318,900,537,190,240,240,0]   # last 0 is placeholder for overall/last route
        rangeSizes = [2,10,70,400,260,800,400,75,130,40,0]
        # sum of rangeSizes is 2054
        
        data = ''
        for rt in Route.objects.all():
            routeAverage=[]
            overallRouteAverage=[]
            
            tempRt = Recording.objects.all().filter(name = rt.name)
            
            i=0
            j=0
            rmax=0.0
            rmin=0.0
            
            rngeMax=rangeMaxs[count]
            rngeSize=rangeSizes[count]
            count=count+1
            
            busy_nw=0.0
            busy=0.0
            
            for trt in tempRt:
                if(trt.name != 'J17 Shankill -> J3 M1/N32/DPT'):
                    
                    rngeLocation = rngeSize - (rngeMax - trt.traveltime)
                    busy_nw = (rngeLocation/rngeSize)
                    
                    routeAverage.append(trt.traveltime)
                    
                    subRouteTotal = subRouteTotal + trt.traveltime
                    i=i+1
                else:
                    overallRouteAverage.append(trt.traveltime)
                    
                    fullRouteTotal = fullRouteTotal + trt.traveltime
                    j=j+1    
                    
            rangeWeight = (rngeSize/2054)
            busy = (busy_nw * rangeWeight)
                    
            data = data + trt.name + ': ' + str(trt.traveltime) + ": busyness = " + str(busy_nw) + ": busynessWeigthed = " + str(busy) + '<br><br/>'
        
        return data
    
    def tests():
        data = ''
        
        bikeSubs = BusynessSub.objects.filter(name = "DublinBikes")
        cpSubs = BusynessSub.objects.filter(name = "CarPark")
        m50Subs = BusynessSub.objects.filter(name = "M50")
        noiseSubs = BusynessSub.objects.filter(name = "NoiseLevel")
        
        
        bizArr_1 = []
        bizArr_2 = []
        bizArr_3 = []
        for i in range(1, 600):
            time = bikeSubs[len(bikeSubs) - i].dateTaken
            bikeVal = bikeSubs[len(bikeSubs) - i].busynessFactor
            cpVal = cpSubs[len(cpSubs) - i].busynessFactor
            m50Val = m50Subs[len(m50Subs) - i].busynessFactor
            nseVal = noiseSubs[len(noiseSubs) - i].busynessFactor
            
            bizFact_1 = ( ( bikeVal* .30) + ( cpVal* .30) + ( m50Val* .10) + ( nseVal* .30) ) 
            bizFact_2 = ( ( bikeVal* .35) + ( cpVal* .35) + ( m50Val* .10) + ( nseVal* .20) ) 
            bizFact_3 = ( ( bikeVal* .30) + ( cpVal* .30) + ( m50Val* .15) + ( nseVal* .25) ) 
            
            rnge = max(bizFact_1, bizFact_2, bizFact_3) - min(bizFact_1, bizFact_2, bizFact_3)
            
            bizArr_1.append(bizFact_1)
            bizArr_2.append(bizFact_2)
            bizArr_3.append(bizFact_3)
            
            data = data + "Busy 1: " +str(bizFact_1) + "<br>"
            data = data + "Busy 2: " +str(bizFact_2) + "<br>"
            data = data + "Busy 3: " +str(bizFact_3) + "<br>"
            data = data + "RANGE SIZE: " +str(rnge) + "<br>"
            data = data + "bk, cp, m50, noise := " + str(bikeVal) + ", "+ str(cpVal) + ", "+ str(m50Val) + ", "+ str(nseVal) + "<br>"
            data = data + "Time: " +str(time) +"<br><br/>"
        
        data = data + "Series 1" + "<br>"
        data = data + "MAX : " + str(max(bizArr_1)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_1)) + "<br><br/>"
        
        data = data + "Series 2" + "<br>"
        data = data + "MAX : " + str(max(bizArr_2)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_2)) + "<br><br/>"
        
        data = data + "Series 3" + "<br>"
        data = data + "MAX : " + str(max(bizArr_3)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_3)) + "<br><br/>"
        return data
    
    
    #template = loader.get_template("myDash.html")
    #return HttpResponse(template.render())
    return HttpResponse(tests())

##########################################
##########################################
##########################################
##########################################
##########################################

def mainBusyness(request):
    
    def createBusynessSub(request, DatasetObject, busynessArg):
        bzSub = BusynessSub.objects.create(dataObj = DatasetObject, busynessFactor = busynessArg)
        bzSub.name = bzSub.dataObj.name
        bzSub.save()
        return
    
    def createBusynessIndex(request, busynessInd):
        busy = BusynessIndex.objects.create(busyness = busynessInd)
        busy.save()
        return
    
    def getDatasetObj(nameArg):
        return DatasetObject.objects.get(name = nameArg)
    
    def getBikes():
        i=0
        subtotal=0
        dso = getDatasetObj('DublinBikes')
        
        data = ''
        for bs in BikeStation.objects.all():
            tempBS = Availability.objects.all().filter(name = bs.name)
            
            for tbs in tempBS:
                data = data + str(i) + ': ' + tbs.name + ': ' + str(tbs.percentFull) + '<br><br/>'
                subtotal = subtotal + tbs.percentFull
                i=i+1 
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average)   
        return data
    
    def getCPs():
        i=0
        subtotal=0
        dso = getDatasetObj('CarPark')
        
        data = ''
        for cp in CP.objects.all():
            tempCP = CapacityLevel.objects.all().filter(name = cp.name)
            
            for tcp in tempCP:
                # THOMASST has recorded only 0 values so I will exlude it for now
                if(tcp.name != 'THOMASST'):
                    data = data + tcp.name + ': ' + str(tcp.percentFull) + '<br><br/>'
                    subtotal = subtotal + tcp.percentFull
                    i=i+1
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average) 
        return data
    
    def getNoiseMeters():
        i=0
        subtotal=0
        dso = getDatasetObj('NoiseLevel')
        
        data = ''
        for mt in Meter.objects.all():
            tempmt = Reading.objects.all().filter(name = mt.name)
            
            for tmt in tempmt:
                data = data + tmt.name + ': ' + str(tmt.aleq) + '<br><br/>'
                subtotal = subtotal + tmt.aleq
                i=i+1
        
        average = (subtotal/i)
        data = data + 'Average: ' + str(average) 
        return data
    
    def getM50s():
        i=0
        j=0
        subRouteTotal=0
        fullRouteTotal=0
        dso = getDatasetObj('M50')
        
        data = ''
        for rt in Route.objects.all():
            tempRt = Recording.objects.all().filter(name = rt.name)
            
            for trt in tempRt:
                if(trt.name != 'J17 Shankill -> J3 M1/N32/DPT'):
                    data = data + trt.name + ': ' + str(trt.traveltime) + '<br><br/>'
                    subRouteTotal = subRouteTotal + trt.traveltime
                    i=i+1
                else:
                    fullRouteTotal = fullRouteTotal + trt.traveltime
                    j=j+1    
        
        subRouteAverage = subRouteTotal/i
        fullRouteAverage = fullRouteTotal/j
        
        data = data + 'subrouteAverage: ' + str(subRouteAverage) + '<br><br/>'
        data = data + 'fullRouteAverage: ' + str(fullRouteAverage) + '<br><br/>'
        
        return data
    
    def getBusynessValues():
        busynessIndex = 0.0
        
        db_dso = getDatasetObj('DublinBikes')
        cp_dso = getDatasetObj('CarPark')
        nl_dso = getDatasetObj('NoiseLevel')
        m50_dso = getDatasetObj('M50')
        
        weigths = [.40, .30, .20, .10]
        
        noiseVal=0
        m50Val=0
        cpVal=0
        bikeVal=0        
        
        noiseVal = noiseLevels.views.noiseLevels(request)
        createBusynessSub(request, nl_dso, noiseVal)
        
        m50Val = m50times.views.m50times(request)
        createBusynessSub(request, m50_dso, m50Val)
        
        cpVal = carParks.views.carParks(request)
        createBusynessSub(request, cp_dso, cpVal)
        
        bikeVal = dublinBikes.views.dubBikes(request)
        createBusynessSub(request, db_dso, bikeVal)
        
        #busynessIndex = ( (m50Val*weigths[0]) + (noiseVal*weigths[1]) + (bikeVal*weigths[3]) )
        
        busynessIndex = ( (m50Val*weigths[0]) + (noiseVal*weigths[1]) + (cpVal*weigths[2]) + (bikeVal*weigths[3]) )
        createBusynessIndex(request, busynessIndex)
        
        ans = "Noise, M50, Bikes, CPs:" + str(noiseVal) + ", " + str(m50Val) + ", " + str(bikeVal) + ", " + str(cpVal)
        #ans=ans + "Busy: " + str(busynessIndex) + ", noise,m50,cp,bk := " + str(noiseVal) + ", " +str(m50Val)+",  "+str(bikeVal)
        #ans=ans + "Busy: " + str(busynessIndex) + ", noise,m50,cp,bk := " + str(noiseVal) + ", " +str(m50Val)+", "+str(cpVal)+", "+str(bikeVal)
        ans = ans+"<br>"+"Busyness: "+str(busynessIndex)
        
        '''busnisses = BusynessIndex.objects.all()
        for i in range(1, 10):
            ans = ans + "-" + str(i) + ": " + str(busnisses[i]) + "<br><br/>"
        '''
        return ans

    #test = dublinBikes.views.dubBikes(request)
    return HttpResponse(getBusynessValues())