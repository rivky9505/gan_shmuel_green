#!/usr/bin/env python3

import requests as req
import datetime
import smtplib


providerAPI ="http://green.develeap.com:8090"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'

def posRequest(urla , data ):
    resp = req.post(urla, data)
    global dataToEmail
    dataToEmail = dataToEmail + "the method Post to " +str(urla)+ " got the response " +str(resp)+'\n'
    with open(logfile, 'a') as the_file:
        the_file.write("the method Post to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Post to " +str(urla)+ " got the response " +str(resp))
    if 200 <= resp.status_code <= 299:
        return True
    return False

def putRequest(urla , data ):
    resp = req.put(urla, data)
    global dataToEmail
    dataToEmail = dataToEmail + "the method Post to " +str(urla)+ " got the response " +str(resp)+'\n'
    with open(logfile, 'a') as the_file:
        the_file.write("the method Put to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Put to " +str(urla)+ " got the response " +str(resp))
    if 200 <= resp.status_code <= 299:
        return True
    return False


#####################################################################################################
#! Prov Tests

def checkHealthProv():
    try:
        return checkRequest(get , provAPI + "/health")
    except:
        global dataToEmail
        dataToEmail = dataToEmail + "Weight ApI is down "+'\n'
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

if checkHealthProv()  == True:
    testResult = provRequests()
endReport(testResult)
