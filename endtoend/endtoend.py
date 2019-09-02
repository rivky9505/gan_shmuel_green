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


#####################################################################################################
#! Weight tests

def checkhealthWeight():
    return checkRequest(get , weightAPI + "/health")

def checkUnknown():
    checkRequest(get , weightAPI + "/unknown")#check unknown list

def checkSession(number):
    checkRequest(get , weightAPI + "/session/" + str(number))#check session

def checkrates():
    checkRequest(get , weightAPI + "/rates")

def weightRequests():
    checkhealthWeight()
    checkUnknown()
    checkSession(1)
    checkSession(2)
    checkSession(3)
    checkrates()


#####################################################################################################
#! Prov Tests

def checkhealthprov():
    return checkRequest(methoda , provAPI + "/health")


weightRequests()
# checkRequest(post , testapipost)
# checkRequest(get , testapi)
