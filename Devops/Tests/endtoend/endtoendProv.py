#!/usr/bin/env python3

import requests as req
import datetime
import smtplib

gmail_user = 'develeapgreen@gmail.com'
gmail_password = 'Aa!123!456'

sent_from = gmail_user
to = ['kobiavshalom@gmail.com', 'yuvalalfassi@gmail.com' , 'ofirami3@gmail.com','danielharsheffer@gmail.com' ,'hire.saar@gmail.com' ,'danarlowski11@gmail.com' ,'89leon@gmail.com' ,'tsinfob@gmail.com' ,'aannoonniimmyy57@gmail.com' ,'roialfassi@gmail.com'  ]

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

subject = "End2End Report: "+ str(dateNow)+'\n'
body = dataToEmail


def startReport():
    with open(logfile, 'a') as the_file:
        the_file.write("End2End Report: "+ str(dateNow)+'\n')
        dataToEmail = dataToEmail + "End2End Report: "+ str(dateNow)+'\n'
        the_file.write("******************************************"+'\n')

def endReport():
    with open(logfile, 'a') as the_file:
        the_file.write("End Report "+'\n')
        the_file.write("******************************************"+'\n')

def checkRequest(methoda , urla):
    resp = req.request(method=methoda, url=urla)
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
    with open(logfile, 'a') as the_file:
        the_file.write("the method Post to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Post to " +str(urla)+ " got the response " +str(resp))
    if 200 <= resp.status_code <= 299:
        return True
    return False

def putRequest(urla , data ):
    resp = req.put(urla, data)
    with open(logfile, 'a') as the_file:
        the_file.write("the method Put to " +str(urla)+ " got the response " +str(resp)+'\n')
        # print("the method Put to " +str(urla)+ " got the response " +str(resp))
    if 200 <= resp.status_code <= 299:
        return True
    return False
    
#####################################################################################################
#! Send mail
def sendMail():

    subject = "End2End Report: "+ str(dateNow)+'\n'
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
#! Main
startReport()

if checkHealthProv()  == True:
    provRequests()

endReport()
sendMail()
# checkRequest(get , "http://green.develeap.com:8080/health")
# checkRequest(get , testapi)
# checkRequest(post , testapipost)

