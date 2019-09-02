#!/usr/bin/env python3

import requests as req


weightAPI = "127.0.0.1:8080"
provAPI ="127.0.0.1:8090"
testapi = "https://api.github.com"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'
testapipost = 'https://httpbin.org/post'

def checkRequest(methoda , urla):
    resp = req.request(method=methoda, url=urla)
    print("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp))
    return(resp)

def posRequest(urla , data)
    resp = req.post(urla, data)
    

#####################################################################################################
#! Weight tests

def checkhealthWeight():
    return checkRequest(get , weightAPI + "/health")

def checkUnknown():
    checkRequest(get , weightAPI + "/unknown")#check unknown list

def checkSession(number):
    checkRequest(get , weightAPI + "/session/" + str(number))#check session

def checkGETrates():
    checkRequest(get , weightAPI + "/rates")

def checkWeightFrom(t1to , t2from , filter)
#TODO check the way we use to and from and fiter
    checkRequest(get , weightAPI + "/weight?from="+str(t1to)+"&to="+str(t2from)+"&filter="str(filter))

def checkItemFrom(itemID,fromt1 , fromt2)
    checkRequest(get , weightAPI + "/item/"+str(itemID)+"?from="+str(fromt1)+"&to="+str(fromt2)+"&filter="str(filter))

def postBatchWeight(filename)
    posRequest(weightAPI + "/batch-weight" , filename)

def postWeight(direction , license , containers ,weight ,unit , force , produce)


def weightRequests():
    checkhealthWeight()
    checkUnknown()
    checkSession(1)
    checkSession(2)
    checkSession(3)
    checkGETrates()


#####################################################################################################
#! Prov Tests

def checkhealthprov():
    return checkRequest(methoda , provAPI + "/health")


weightRequests()
# checkRequest(post , testapipost)
# checkRequest(get , testapi)
