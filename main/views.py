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
from datetime import datetime

import datetime
import math
import noiseLevels.views
import m50times.views
import dublinBikes.views
import carParks.views
from boto.dynamodb.condition import NULL
from statistics import mean

def home(request):
    
    allBusynessz = BusynessIndex.objects.all()
    
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
    bizness = round(bizness, 3)
    ################################################
    
    ########### Line Graph 1 Data #####################
    bizys1 = []
    bizys2 = []
    bizys3 = []
    time1 = []
    time2 = []
    time3 = []
    sze = len(allBusynessz)
    
    for i in range(13):
        tempBiz1 = allBusynessz.get(id = (sze-(i-1)))
        bizys1.append(tempBiz1.busyness)
        
        dt = datetime.datetime.strptime(str(tempBiz1.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        dt_in_ms = int(dt)*1000
        
        time1.append(dt_in_ms)
        #tmptym = (tempBiz.dateTaken).time()
        #tmptym = datetime.datetime.now() - datetime.timedelta(minutes=(i * 5))
        #tmptym = ((tempBiz.dateTaken) - datetime(1970, 1, 1)).total_seconds() 
        
        
        #times1.append(tmptym)
    ################################################
    
    ########### Line Graph 2 Data #####################
    for i in range(2000):
        indx = sze-(i-1)
        
        if (indx == 1780) or (indx == 1680) :
            i=i+1   
            indx = sze-(i-1)
        
        tempBiz2 = allBusynessz.get(id = (indx))
            
        bizys2.append(tempBiz2.busyness)
        
        a = datetime.datetime.strptime(str(tempBiz2.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        d_in_ms = int(a)*1000
        #a = a.timestamp() * 1000
        time2.append(d_in_ms)
    ################################################
    
    ########### Bar Chart Data #####################
    ################################################
    
    ########### Line Graph 3 Data #####################
    mondays = []
    for i in range(3000):
        indx = sze-(i-1)
        
        if (indx == 1780) or (indx == 1680) :
            i=i+1   
            indx = sze-(i-1)
        
        tempBiz3 = allBusynessz.get(id = (indx))
            
        bizys3.append(tempBiz3.busyness)
        
        #if(tempBiz3.dateTaken.day == 0):
         #   mondays.append(tempBiz3)
        
        a = datetime.datetime.strptime(str(tempBiz3.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        d_in_ms = int(a)*1000
        #a = a.timestamp() * 1000
        time3.append(d_in_ms)
    ################################################
    
    ### DATASET CONTEXTS ###########################
    cps = []
    bikes = []
    noises = []
    
    cptimes = []
    biketimes = []
    noisetimes = []
    
    szeC = len(cpSubs)-1
    szeB = len(bikeSubs)-1
    szeN = len(noiseSubs)-1
    
    for i in range(3000):
        indxC = szeC-(i)
        indxB = szeB-(i)
        indxN = szeN-(i)
        
        tempCP = cpSubs[indxC]
        tempBk = bikeSubs[indxB]
        tempNse = noiseSubs[indxN]
            
        cps.append(tempCP.busynessFactor)
        bikes.append(tempBk.busynessFactor)
        noises.append(tempNse.busynessFactor)
        
        c = datetime.datetime.strptime(str(tempCP.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        b = datetime.datetime.strptime(str(tempBk.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        n = datetime.datetime.strptime(str(tempNse.dateTaken), '%Y-%m-%d %H:%M:%S.%f+00:00').strftime('%s')
        
        d_in_msC = int(c)*1000
        d_in_msB = int(b)*1000
        d_in_msN = int(n)*1000
        
        #a = a.timestamp() * 1000
        
        cptimes.append(d_in_msC)
        biketimes.append(d_in_msB)
        noisetimes.append(d_in_msN)
    ################################################
    
    ### Pass Required Data to our Context ##########
    context = {
        "busyIndNow": bizness,
        "donutData": dat,
        "line1bizs" : bizys1,
        "line2bizs" : bizys2,
        "line3bizs" : bizys3,
        "line1times" : time1,
        "line2times" : time2,
        "line3times" : time3,
        
        "cps" : cps,
        "cptimes" : cptimes, 
        
        "bikes" : bikes,
        "biketimes" : biketimes, 
        
        "noises" : noises,
        "noisetimes" : noisetimes, 
        
        #"mon" : mondays,
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
        
        busys = BusynessIndex.objects.all()
        
        bizArr_1 = []
        
        totl = 0.0
        
        bizArr_2 = []
        bizArr_3 = []
        for i in range(1, 800):
            time = bikeSubs[len(bikeSubs) - i].dateTaken
            bikeVal = bikeSubs[len(bikeSubs) - i].busynessFactor
            cpVal = cpSubs[len(cpSubs) - i].busynessFactor
            m50Val = m50Subs[len(m50Subs) - i].busynessFactor
            nseVal = noiseSubs[len(noiseSubs) - i].busynessFactor
            bizVal = busys[len(busys) - i].busyness
            
            bizFact_1 = ( ( bikeVal* .25) + ( cpVal* .20) + ( m50Val* .05) + ( nseVal* .50) ) 
            bizFact_2 = ( ( bikeVal* .30) + ( cpVal* .25) + ( m50Val* .05) + ( nseVal* .40) ) 
            bizFact_3 = bizVal
            #bizFact_3 = ( ( bikeVal* .30) + ( cpVal* .25) + ( m50Val* .05) + ( nseVal* .40) ) 
            
            #rnge = max(bizFact_1, bizFact_2, bizFact_3) - min(bizFact_1, bizFact_2, bizFact_3)
            
            bizArr_1.append(bizFact_1)
            #totl = totl + bizFact_1
            
            bizArr_2.append(bizFact_2)
            bizArr_3.append(bizFact_3)
            
            data = data + "Busy 1: " +str(bizFact_1) + "<br>"
            data = data + "Busy 2: " +str(bizFact_2) + "<br>"
            data = data + "Busy 3 real: " +str(bizFact_3) + "<br>"
            #data = data + "Busy 3: " +str(bizFact_3) + "<br>"
            #data = data + "RANGE SIZE: " +str(rnge) + "<br>"
            #data = data + "bk, cp, m50, noise := " + str(bikeVal) + ", "+ str(cpVal) + ", "+ str(m50Val) + ", "+ str(nseVal) + "<br>"
            data = data + "Time: " +str(time) +"<br><br/>"
        
        data = data + "Series 1" + "<br>"
        data = data + "MAX : " + str(max(bizArr_1)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_1)) + "<br><br/>"
        
        data = data + "Series 2" + "<br>"
        data = data + "MAX : " + str(max(bizArr_2)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_2)) + "<br><br/>"
        
        data = data + "Real 3" + "<br>"
        data = data + "MAX : " + str(max(bizArr_3)) + "<br>"
        data = data + "MIN : " + str(min(bizArr_3)) + "<br><br/>"
        
        mean1 = sum(bizArr_1) / len(bizArr_1)
        mean2 = sum(bizArr_2) / len(bizArr_2)
        mean3 = sum(bizArr_3) / len(bizArr_3)
        
        m1s=0.0
        m2s=0.0
        m3s=0.0
        for i in range(0, len(bizArr_1)):            
            m1s = m1s + ( (bizArr_1[i] - mean1) * (bizArr_1[i] - mean1) ) 
            m2s = m2s + ( (bizArr_2[i] - mean2) * (bizArr_2[i] - mean2) )
            m3s = m3s + ( (bizArr_3[i] - mean2) * (bizArr_3[i] - mean3) )
            
        std_1 = math.sqrt( m1s / len(bizArr_1) )
        std_2 = math.sqrt( m2s / len(bizArr_1) )
        std_3 = math.sqrt( m3s / len(bizArr_1) )
        
        
        #data = data + "Series 3" + "<br>"
        #data = data + "MAX : " + str(max(bizArr_3)) + "<br>"
        #data = data + "MIN : " + str(min(bizArr_3)) + "<br><br/>"
        
        data = data + "S1 Sd: " + str(std_1) + "<br>"
        data = data + "S2 Sd: " + str(std_2) + "<br>"
        data = data + "S3 Sd: " + str(std_3) + "<br>"
        
        return data
    
    def tests2():
        data = ''
        data = data + "Standard Deviation of Datasets Page" + "<br>"
        data = data + "-----------------------------------" + "<br></br>"
        bikeSubs = BusynessSub.objects.filter(name = "DublinBikes")
        cpSubs = BusynessSub.objects.filter(name = "CarPark")
        m50Subs = BusynessSub.objects.filter(name = "M50")
        noiseSubs = BusynessSub.objects.filter(name = "NoiseLevel")
        
        
        nArr =[]
        bkArr = []
        cpArr = []
        m50arr = []
        
        nseS = 0.0
        bkeS = 0.0
        cpS = 0.0
        m5S = 0.0
        for i in range(1, 1300):
            #time = bikeSubs[len(bikeSubs) - i].dateTaken
            bikeVal = bikeSubs[len(bikeSubs) - i].busynessFactor
            cpVal = cpSubs[len(cpSubs) - i].busynessFactor
            m50Val = m50Subs[len(m50Subs) - i].busynessFactor
            nseVal = noiseSubs[len(noiseSubs) - i].busynessFactor
        
            bkArr.append(bikeVal)
            nArr.append(nseVal)
            m50arr.append(m50Val)
            
            if(cpVal != 95):
                cpArr.append(cpVal)
        
        bAv = sum(bkArr) / len(bkArr)
        cAv = sum(cpArr) / len(cpArr)
        nAv = sum(nArr) / len(nArr)
        mAv = sum(m50arr) / len(m50arr)
        
        for i in range(0, len(bkArr)):            
            nseS = nseS + ( (nArr[i] - nAv) * (nArr[i] - nAv) ) 
            bkeS = bkeS + ( (bkArr[i] - bAv) * (bkArr[i] - bAv) )
            m5S = m5S + ( (m50arr[i] - mAv) * (m50arr[i] - mAv) )
            
        sz = len(cpArr)    
        for i in range(0, sz):
            cpS = cpS + ( (cpArr[i] - cAv) * (cpArr[i] - cAv) )
            
        std_cp = math.sqrt( cpS / sz )
        std_bk = math.sqrt( bkeS / 250 )
        std_ns = math.sqrt( nseS / 250 )
        std_m50 = math.sqrt( m5S / 250 )
        
        data = data + "STD CP: " + str(std_cp) + "<br>"
        data = data + "Min, Max: " + str(min(cpArr)) + ", " + str(max(cpArr)) + "<br></br>"
        
        data = data + "STD Bikes: " + str(std_bk) + "<br>"
        data = data + "Min, Max: " + str(min(bkArr)) + ", " + str(max(bkArr)) + "<br></br>"
        
        data = data + "STD Noises: " + str(std_ns) + "<br>"
        data = data + "Min, Max: " + str(min(nArr)) + ", " + str(max(nArr)) + "<br></br>"
        
        data = data + "STD m50: " + str(std_m50) + "<br>"
        data = data + "Min, Max: " + str(min(m50arr)) + ", " + str(max(m50arr)) + "<br></br>"
        
        '''
        noiseVal = noiseLevels.views.noiseLevels(request)
        #createBusynessSub(request, nl_dso, noiseVal)
        
        #if m50times.views.m50times(request) != NULL:
        m50Val = m50times.views.m50times(request)
        #else:
        #   m50Val = 25    
        #createBusynessSub(request, m50_dso, m50Val)
        
        cpVal = carParks.views.carParks(request)
        #createBusynessSub(request, cp_dso, cpVal)
        
        bikeVal = dublinBikes.views.dubBikes(request)
        #createBusynessSub(request, db_dso, bikeVal)
        
        #data = data + "n,m,c,b:= " + noiseVal + ", " + m50Val + ", " + cpVal + ", " + bikeVal
        
        data=data + "N: " + str(noiseVal) + "<br>"
        data=data + "M50: " + str(m50Val) + "<br>"
        data=data + "cp: " + str(cpVal) + "<br>"
        data=data + "b: " + str(bikeVal) + "<br>"
        '''
        return data
    
    
    #template = loader.get_template("myDash.html")
    #return HttpResponse(template.render())
    return HttpResponse(tests2())

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
        
        weigths = [.40, .30, .25, .05]
        
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
        
        #busynessIndex = ( (m50Val*weigths[3]) + (noiseVal*weigths[0]) + (cpVal*weigths[1]) + (bikeVal*weigths[2]) )
        busynessIndex = ( (noiseVal*weigths[0]) + (bikeVal*weigths[1]) + (cpVal*weigths[2]) + (m50Val*weigths[3]) )
        
        createBusynessIndex(request, busynessIndex)
        
        ans = "Noise, M50, Bikes, CPs:" + str(noiseVal) + ", " + str(m50Val) + ", " + str(bikeVal) + ", " + str(cpVal)
        #ans=ans + "Busy: " + str(busynessIndex) + ", noise,m50,cp,bk := " + str(noiseVal) + ", " +str(m50Val)+",  "+str(bikeVal)
        #ans=ans + "Busy: " + str(busynessIndex) + ", noise,m50,cp,bk := " + str(noiseVal) + ", " +str(m50Val)+", "+str(cpVal)+", "+str(bikeVal)
        ans = ans+"<br>"+"Busyness: "+str(busynessIndex)
        
        '''busnisses = BusynessIndex.objects.all()
        for i in range(1, 10):
            ans = ans + "-" + str(i) + ": " + str(busnisses[i]) + "<br><br/>"
        '''
        #ans = str(noiseVal) 
        #ans = str(m50Val)
        ans = str(noiseVal) + ", " +str(m50Val) + ", " +str(bikeVal) + ", " +str(cpVal) + ", " +str(busynessIndex)
        #ans = str(noiseVal) + ", " +str(m50Val)
        return ans

    #test = dublinBikes.views.dubBikes(request)
    return getBusynessValues()