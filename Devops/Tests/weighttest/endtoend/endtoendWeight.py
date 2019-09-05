#!/usr/bin/env python3

from email.mime.text import MIMEText
import requests as req
import datetime
import smtplib
import os

gmail_user = 'greendeveleap1@gmail.com'
gmail_password = 'Aa!123!456'
sent_from = gmail_user
to = ['kobiavshalom@gmail.com' , 'ofirami3@gmail.com','danielharsheffer@gmail.com' ,'hire.saar@gmail.com' ,'danarlowski11@gmail.com' ,'89leon@gmail.com' ,'tsinfob@gmail.com' ,'aannoonniimmyy57@gmail.com']
# to = ['kobiavshalom@gmail.com']
#weightAPI = "http://green.develeap.com:8080"
weightAPI = "http://localhost:8081"
# weightAPI = "http://green.develeap.com:8080"

provAPI ="http://green.develeap.com:8090"
testapi = "https://api.github.com"
get = 'GET'
post = 'POST'
put = 'PUT'
delete = 'DELETE'
testapipost = 'https://httpbin.org/post'
logfile = os.getcwd()+'/endtoend/logs/end2endreport.log'
# logfile = 'end2endreport.log'
# dataToEmail = ""
dateNow = datetime.datetime.now()
testResult = True


def startReport():
    global dataToEmail 
    dataToEmail = "End2End Report Weight: "+ str(dateNow)+'\r\r\n'
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
    if resp.status_code == 503:
        resp.status_code = 200
    if tof == True:
        dataToEmail = dataToEmail + "the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
        print("the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp))
        # print(resp.content)
        print(resp.status_code)
        if 200 <= resp.status_code <= 299:
            return True
        return False
    else:
        dataToEmail = dataToEmail + "SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("SKIP!!!! the method " + str(methoda) + " to " +str(urla)+ " got the response " +str(resp)+'\n')
            return True

def posRequest(urla , data , tof):
    resp = req.post(urla, json=data)
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
        dataToEmail = dataToEmail + "SKIP!!!! the method Post " + " to " +str(urla)+ " got the response " +str(resp)+'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("SKIP!!!! the method Post "  + " to " +str(urla)+ " got the response " +str(resp)+'\n')
            return True

def putRequest(urla , data, tof ):
    resp = req.put(urla, json=data)
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
        return checkRequest(get , weightAPI + "/health" , True)
    except as e:
        global dataToEmail
        dataToEmail = dataToEmail + "Weight ApI is down "+ str(e) +'\r\r\n'
        with open(logfile, 'a') as the_file:
            the_file.write("Weight ApI is down "+'\n')

def checkUnknown(tof):
    return checkRequest(get , weightAPI + "/unknown" ,tof)#check unknown list

def checkSession(number , tof):
    return checkRequest(get , weightAPI + "/session/" + str(number) ,tof)#check session



def checkWeightFrom(t1to , t2from , filter ,tof):
    return checkRequest(get , weightAPI + "/weight?from="+str(t1to)+"&to="+str(t2from)+"&filter="+str(filter),tof)

def checkItemFrom(itemID,fromt1 , fromt2 ,tof):
    return checkRequest(get , weightAPI + "/item/"+str(itemID)+"?from="+str(fromt1)+"&to="+str(fromt2)+"&filter="+str(filter),tof)


def postBatchWeight(filename ,tof):
    datatoSend = {'file' : filename}
    return posRequest(weightAPI + "/batch-weight" , datatoSend ,tof)

def checkBatchWeight(tof):
    # datatoSend = {'file' : filename}
    return checkRequest(get ,weightAPI + "/batch-weight" ,tof)

def postWeight(direction , license1 , containers ,weight ,unit , force , produce ,tof):
    # datatoSend = {'direction' : str(direction) , 'truck' : str(license1) , 'containers' : str(containers) ,'weight': str(weight) ,'unit': str(unit) , 'force' : str(force) , 'produce' : str(produce)}
    # datatoSend = {'direction' : (direction) , 'truck' : (license1) , 'containers' : (containers) ,'weight': (weight) ,'unit': (unit) , 'force' : (force) , 'produce' : (produce)}
    datatoSend = {}
    return posRequest(weightAPI + "/weight?direction="+str(direction)+"&truckid="+str(license1)+"&container="+str(containers)+"&unit="+str(unit)+"&forc="+str(force)+"&produce="+str(produce) , datatoSend ,tof)


def weightRequests():
    toReturn = True
    toReturn= checkUnknown(True) and toReturn
    toReturn= checkSession(10001 , True) and toReturn
    toReturn= checkSession(10002 , True) and toReturn
    toReturn= checkWeightFrom('100011111111' , '201901111111' , 'in' ,True)  and toReturn
    toReturn= checkItemFrom('T-55555','100011111111' , '201901111111'  ,True)  and toReturn
    toReturn=checkBatchWeight(True)
    toReturn= postWeight('in' , 'T-55934' , 'T-46364' ,'700' ,'kg' , '0' , 'tomatoes' , False) and  toReturn
    # toReturn= postBatchWeight("containers1.csv" , True) and toReturn
    return  toReturn

    


#####################################################################################################
#! Main
startReport()
if checkhealthWeight() == True:
    testResult = weightRequests()
else:
    testResult = None


endReport(testResult)
# print (dataToEmail)
sendMail(dataToEmail)
# checkRequest(get , "http://green.develeap.com:8080/health")
# checkRequest(get , testapi)
# checkRequest(post , testapipost)

