import os

logfile = os.getcwd()+'/endtoend/logs/end2endreport.log'
file=open(logfile)
data = file.readlines()
lastline = data[-1]
worddata = lastline.split()
if worddata[-1] == "True":
    print (0)
else:
    print (1)