# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 13:24:56 2021

@author: EBB
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_content = "Bu ebb tarafından oluşturulan otomatik test mailidir"

#The mail addresses and password
sender_address = 'eopy.testmail@gmail.com'
sender_pass = 'Eopy123456@'



def sendMail(receiver):
    receiver_address = receiver
    #Setup the MIME



    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'EOPY VIBRATION PROJECT TEST MAIL'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')