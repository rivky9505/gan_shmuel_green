import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "my@gmail.com"
receiver_email1 = "your@gmail.com"
receiver_email2 = "your@gmail.com"
receiver_email3 = "your@gmail.com"
receiver_email4 = "your@gmail.com"
receiver_email5 = "your@gmail.com"
receiver_email6 = "your@gmail.com"
receiver_email7 = "your@gmail.com"
receiver_email8 = "your@gmail.com"
receiver_email9 = "your@gmail.com"
password = "Type your password and press enter:"

datatosend = []
with open('end2endreport.log') as fp:
    line = fp.readline()
        while line:
            datatosend.append(line.strip)
            line = fp.readline()


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email1, datatosend)
    server.sendmail(sender_email, receiver_email2, datatosend)
    server.sendmail(sender_email, receiver_email3, datatosend)
    server.sendmail(sender_email, receiver_email4, datatosend)
    server.sendmail(sender_email, receiver_email5, datatosend)
    server.sendmail(sender_email, receiver_email6, datatosend)
    server.sendmail(sender_email, receiver_email7, datatosend)
    server.sendmail(sender_email, receiver_email8, datatosend)
    server.sendmail(sender_email, receiver_email9, datatosend)
    
    

