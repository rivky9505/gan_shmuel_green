#!/usr/bin/env python3
from email.mime.text import MIMEText
import requests as req
import datetime
import smtplib
import os

gmail_user = 'develeapgreen@gmail.com'
gmail_password = 'Aa!123!456'
#'yuvalalfassi@gmail.com'
sent_from = gmail_user
to = ['kobiavshalom@gmail.com' , 'ofirami3@gmail.com','danielharsheffer@gmail.com' ,'hire.saar@gmail.com' ,'danarlowski11@gmail.com' ,'89leon@gmail.com' ,'tsinfob@gmail.com' ,'aannoonniimmyy57@gmail.com']

weightAPI = "http://green.develeap.com:8080"
provAPI ="http://localhost:8089"
testapi = "https://api.github.com"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'
testapipost = 'https://httpbin.org/post'
logfile =  os.getcwd()+'/endtoend/logs/end2endreport.log'
# logfile = 'end2endreport.log'

# dataToEmail = ""
dateNow = datetime.datetime.now()
testResult = True


def startReport():
    global dataToEmail 
    dataToEmail = "End2End Report Provider: "+ str(dateNow)+'\r\r\n'
    with open(logfile, 'a') as the_file:
        the_file.write("End2End Report Provider: "+ str(dateNow)+'\n')
        the_file.write("******************************************"+'\n')
    

def endReport(testResult1):
    global dataToEmail 
    # print ("data to email before " + dataToEmail)
    dataToEmail = dataToEmail + "End2End Report: "+ "End Report "+ str(testResult1) +'\r\r\n'
    with open(logfile, 'a') as the_file:
        the_file.write("End Report "+str(testResult1) +'\n')


def checkRequest(methoda , urla , tof):
    resp = req.request(method=methoda, url=urla)
    global dataToEmail
    if tof == True:
        dataToEmail = dataToEmail + "the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
        print("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp))
        # print(resp.content)
        print(resp.status_code)
        if 200 <= resp.status_code <= 299:
            return True
        if resp.status_code == 503:
            return True
        return False
    else:
        dataToEmail = dataToEmail + "SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
            return True

def posRequest(urla , data , tof):
    resp = req.post(urla, data)
    global dataToEmail   
    if tof == True:
        dataToEmail = dataToEmail + "the method Post to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("the method Post to " +str(urla)+ " got the response " +str(resp)+'\n')
            # print("the method Post to " +str(urla)+ " got the response " +str(resp))
        if 200 <= resp.status_code <= 299:
            return True
        return False
    else:
        dataToEmail = dataToEmail + "SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
            return True

def putRequest(urla , data, tof ):
    resp = req.put(urla, data)
    global dataToEmail
    if tof == True:
        dataToEmail = dataToEmail + "the method Put to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("the method Put to " +str(urla)+ " got the response " +str(resp)+'\n')
            # print("the method Put to " +str(urla)+ " got the response " +str(resp))
        if 200 <= resp.status_code <= 299:
            return True
        return False
    else:
        dataToEmail = dataToEmail + "SKIP!!!! the method Put to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("SKIP!!!! the method Put to " +str(urla)+ " got the response " +str(resp)+'\n')
            return True
    
#####################################################################################################
#! Send mail
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
        print ('step 1!')
        server.ehlo()
        print ('step 2!')
        server.login(gmail_user, gmail_password)
        print ('step 3')
        server.sendmail(sent_from, to, email_text)
        print ('step 4')
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')

#####################################################################################################
#! Prov Tests

def checkHealthProv():
    try:
        global testResult 
        testResult = checkRequest(get , provAPI + "/health" , True)
        return testResult
    except:
        global dataToEmail
        dataToEmail = dataToEmail + "Provider ApI is down "+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("Provider ApI is down"+'\n')


def checkGetRatesPROV(tof):
    return checkRequest(get , provAPI + "/rates" ,tof)

def checkGetBillPROV(id1 , fromt1 ,tot2 , tof):
    return checkRequest(get , provAPI + "/bill/" + str(id1)+"?from=" + str(fromt1) + "&to=" + str(tot2) , tof)



def checkPostProvider(pName , tof):
    datatoSend = {'name': pName}
    posRequest(provAPI+"/provider" , datatoSend, tof)

def checkPostRates(filename , tof):
    datatoSend = {'filename' : filename}
    posRequest(provAPI+"/rates" , datatoSend ,tof)

def postTruck(pName , id1 , tof):
    datatoSend = {'provider': pName , 'id':id1}
    posRequest(provAPI+"/truck/"+str(pName) , datatoSend , tof)

def putTruck(id1 , tof):
    datatoSend = {'id':id1}
    putRequest(provAPI+"/truck/"+str(id1) , datatoSend , tof)

def putProvider(pName , tof):
    datatoSend = {'id': pName}
    putRequest(provAPI+"/provider/"+str(pName) , datatoSend ,tof)

# data={'number': 12524, 'type': 'issue', 'action': 'show'}

def provRequests():
    toReturn = True
    toReturn= checkGetRatesPROV(True) and toReturn 
    toReturn= checkGetBillPROV('10003' , '20150101000000' ,'20200101000000' , False) and toReturn
    toReturn= checkPostProvider(1111111 , True,) and toReturn
    toReturn= checkPostRates('rates.xlsx' , True) and toReturn 
    toReturn= putProvider(1111111 , True) and toReturn
    toReturn= postTruck(1111111 , 2212 , True) and toReturn
    toReturn= putTruck(2212 , True) and toReturn
    return  toReturn

#####################################################################################################
#! Main
startReport()

if checkHealthProv()  == True:
    testResult = provRequests()
else: 
    testResult = None
    
endReport(testResult)
# print (dataToEmail)
sendMail(dataToEmail)
# checkRequest(get , "http://green.develeap.com:8080/health")
# checkRequest(get , testapi)
# checkRequest(post , testapipost)

