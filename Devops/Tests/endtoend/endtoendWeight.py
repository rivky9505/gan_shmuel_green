#!/usr/bin/env python3

import requests as req
import datetime
import smtplib

gmail_user = 'develeapgreen@gmail.com'
gmail_password = 'Aa!123!456'
#'yuvalalfassi@gmail.com'
sent_from = gmail_user
to = ['kobiavshalom@gmail.com' , 'ofirami3@gmail.com','danielharsheffer@gmail.com' ,'hire.saar@gmail.com' ,'danarlowski11@gmail.com' ,'89leon@gmail.com' ,'tsinfob@gmail.com' ,'aannoonniimmyy57@gmail.com']

weightAPI = "http://green.develeap.com:8080"
provAPI ="http://green.develeap.com:8090"
testapi = "https://api.github.com"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'
testapipost = 'https://httpbin.org/post'
logfile = 'end2endreport.log'
# dataToEmail = ""
dateNow = datetime.datetime.now()
testResult = True


def startReport():
    global dataToEmail 
    dataToEmail = "End2End Report Weight: "+ str(dateNow)+'\n'
    with open(logfile, 'a') as the_file:
        the_file.write("End2End Report Weight: "+ str(dateNow)+'\n')
        the_file.write("******************************************"+'\n')
    

def endReport(testResult1):
    global dataToEmail 
    # print ("data to email before " + dataToEmail)
    dataToEmail = dataToEmail + "End2End Report: "+ "End Report "+ str(testResult1) +'\n'
    with open(logfile, 'a') as the_file:
        the_file.write("End Report "+str(testResult1) +'\n')
        the_file.write("******************************************"+'\n')

def checkRequest(methoda , urla):
    resp = req.request(method=methoda, url=urla)
    global dataToEmail
    dataToEmail = dataToEmail + "the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)
    with open(logfile, 'a') as the_file:
        the_file.write("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
    print("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp))
    # print(resp.content)
    print(resp.status_code)
    if 200 <= resp.status_code <= 299:
        return True
    return False

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
#! Send mail
def sendMail(dataToEmail):

    subject = "End2End Report: "+ str(dateNow)
    body = dataToEmail
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')

#####################################################################################################
#! Weight tests

def checkhealthWeight():
    try: 
        return checkRequest(get , weightAPI + "/health")
    except:
        global dataToEmail
        dataToEmail = dataToEmail + "Weight ApI is down "+'\n'
        with open(logfile, 'a') as the_file:
            the_file.write("Weight ApI is down "+'\n')

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
if checkhealthWeight() == True:
    testResult = weightRequests()

if checkHealthProv()  == True:
    testResult = provRequests()
endReport(testResult)
# print (dataToEmail)
sendMail(dataToEmail)
# checkRequest(get , "http://green.develeap.com:8080/health")
# checkRequest(get , testapi)
# checkRequest(post , testapipost)

