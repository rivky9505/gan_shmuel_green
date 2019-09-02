#!/usr/bin/env python3

import requests as req
import datetime

weightAPI = "http://green.develeap.com:8080"
provAPI ="http://green.develeap.com:8090"
testapi = "https://api.github.com"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'
testapipost = 'https://httpbin.org/post'
logfile = 'end2endreport.log'
dataToEmail = ''
dateNow = datetime.datetime.now()

def startReport():
    with open(logfile, 'a') as the_file:
        the_file.write("End2End Report: "+ str(dateNow)+'\n')
        the_file.write("******************************************"+'\n')
        dataToEmail = dataToEmail + "End2End Report: "+ str(dateNow)+'\n'
        dataToEmail = dataToEmail + "******************************************"+'\n'

def endReport():
    with open(logfile, 'a') as the_file:
        the_file.write("End Report "+'\n')
        the_file.write(End Report "+'\n')
        dataToEmail = dataToEmail + "End2End Report: "+ str(dateNow)+'\n'
        dataToEmail = dataToEmail + "******************************************"+'\n'

def checkRequest(methoda , urla):
    resp = req.request(method=methoda, url=urla)
    with open(logfile, 'a') as the_file:
        the_file.write("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
    print("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp))
    # print(resp.content)
    print(resp.status_code)
    dataToEmail = dataToEmail + "the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'n'
    if 200 <= resp.status_code <= 299:
        return True
    return False

def posRequest(urla , data ):
    resp = req.post(urla, data)
    with open(logfile, 'a') as the_file:
        the_file.write("the method Post to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Post to " +str(urla)+ " got the response " +str(resp))
    dataToEmail = dataToEmail + "the method Post to " +str(urla)+ " got the response " +str(resp)+'\n'
    if 200 <= resp.status_code <= 299:
        return True
    return False

def putRequest(urla , data ):
    resp = req.put(urla, data)
    with open(logfile, 'a') as the_file:
        the_file.write("the method Put to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Put to " +str(urla)+ " got the response " +str(resp))
    dataToEmail = dataToEmail + "the method Put to " +str(urla)+ " got the response " +str(resp)+'\n'
    if 200 <= resp.status_code <= 299:
        return True
    return False
    

#####################################################################################################
#! Weight tests

def checkhealthWeight():
    try: 
        return checkRequest(get , weightAPI + "/health")
    except:
        with open(logfile, 'a') as the_file:
            the_file.write("Weight ApI is down"+'\n')

def checkUnknown():
    checkRequest(get , weightAPI + "/unknown")#check unknown list

def checkSession(number):
    checkRequest(get , weightAPI + "/session/" + str(number))#check session

def checkGETrates():
    checkRequest(get , weightAPI + "/rates")

def checkWeightFrom(t1to , t2from , filter):
#TODO check the way we use to and from and fiter
    checkRequest(get , weightAPI + "/weight?from="+str(t1to)+"&to="+str(t2from)+"&filter="+str(filter))

def checkItemFrom(itemID,fromt1 , fromt2):
    checkRequest(get , weightAPI + "/item/"+str(itemID)+"?from="+str(fromt1)+"&to="+str(fromt2)+"&filter="+str(filter))


def postBatchWeight(filename):
    datatoSend = {'file' : filename}
    posRequest(weightAPI + "/batch-weight" , datatoSend)

def postWeight(direction , license1 , containers ,weight ,unit , force , produce):
    # datatoSend = {'direction' : str(direction) , 'truck' : str(license1) , 'containers' : str(containers) ,'weight': str(weight) ,'unit': str(unit) , 'force' : str(force) , 'produce' : str(produce)}
    datatoSend = {'direction' : (direction) , 'truck' : (license1) , 'containers' : (containers) ,'weight': (weight) ,'unit': (unit) , 'force' : (force) , 'produce' : (produce)}
    posRequest(weightAPI + "/weight" , datatoSend)


def weightRequests():
    toReturn = True
    toReturn= checkUnknown() and toReturn
    toReturn= checkSession(1) and toReturn
    toReturn= checkSession(2) and toReturn
    toReturn= checkGETrates() and toReturn
    toReturn= postWeight('in' , 'na' , 55 ,50 ,'kg' , True , "tomato") and toReturn
    return  toReturn

    


#####################################################################################################
#! Prov Tests

def checkHealthProv():
    try:
        return checkRequest(get , provAPI + "/health")
    except:
        with open(logfile, 'a') as the_file:
            the_file.write("Provider ApI is down"+'\n')


def checkGetRatesPROV():
    return checkRequest(get , provAPI + "/rates")

def checkGetBillPROV(id1 , fromt1 ,tot2):
    return checkRequest(get , provAPI + "/bill/" + str(id1)+"?from=" + str(fromt1) + "&to=" + str(tot2))



def checkPostProvider(pName):
    datatoSend = {'name': pName}
    posRequest(provAPI+"/provider" , datatoSend)

def checkPostRates(file , product , rate , scope):
    datatoSend = {'File' : file , 'Product' : product ,'Rate': rate ,'Scope': scope}
    posRequest(provAPI+"/rates" , datatoSend)

def postTruck(pName , id1):
    datatoSend = {'provider': pName , 'id':id1}
    posRequest(provAPI+"/truck/"+str(pName) , datatoSend)

def putTruck(id1):
    datatoSend = {'id':id1}
    putRequest(provAPI+"/truck/"+str(id1) , datatoSend)

def putProvider(pName):
    datatoSend = {'id': pName}
    putRequest(provAPI+"/provider/"+str(pName) , datatoSend)

# data={'number': 12524, 'type': 'issue', 'action': 'show'}

def provRequests():
    toReturn = True
    toReturn= checkGetRatesPROV() and toReturn
    toReturn= checkPostProvider(1111111) and toReturn
    toReturn= putProvider(1111111) and toReturn
    toReturn= postTruck(1111111 , 2212) and toReturn
    toReturn= putTruck(2212)and toReturn
    return  toReturn

#####################################################################################################
#! Main
startReport()
if checkhealthWeight() == True:
    weightRequests()

if checkHealthProv()  == True:
    provRequests()

endReport()
# checkRequest(get , "http://green.develeap.com:8080/health")
# checkRequest(get , testapi)
# checkRequest(post , testapipost)
