################################################################################################
#                                       SendIP.py
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program is used to send an email containing the machines external IP
#  
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2017-01-10 GLC   Added code to obtain and email out the NGROK address to support 
#                            Alexa integration
#  1.2      2019-01-20 GLC   Hardened DB security - fixed typo on indents
################################################################################################
import socket
import fcntl
import struct
import ipgetter
import sys
import MySQLdb
# import time functions
import datetime
from datetime import date
import time
from time import sleep
import smtplib 
import mimetypes
import email 
import email.mime.application 
import os
import json
from getpw import getpass

################################################################################################
###################### Function to write to the event log table ################################
################################################################################################

def write_log(Log_From, Log_Text):

  dbpass = getpass()

  db = MySQLdb.connect (host   = "localhost",
                        user   = "TCROOT9000",
                        passwd = dbpass,
                        db     = "BoilerControl")  

  log_cursor = db.cursor()
 
  sql = """INSERT INTO log(Log_From, Log_Text) VALUES ('"""+Log_From+"""','"""+Log_Text+"""')""" 

  try:
     log_cursor.execute(sql)
     db.commit()

  except MySQLdb.Error as err:
     db.rollback()
     print ("***** Error on log insert: ERROR: {}".format(err))

  log_cursor.close() 	
  db.close()

################################################################################################  
############  Clever function to get the internal router IP address of the PI ##################
################I didn't write this, some clever chap on the internet wrote it, ta!#############
################################################################################################  

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])  
  
  
  
  
################################################################################################
################################ Function to send and email ####################################
################################################################################################

def send_alert(subject, msgbody):
  
  dbpass = getpass()


  db = MySQLdb.connect (host   = "localhost",
                       user   = "TCROOT9000",
                       passwd = dbpass,
                       db     = "BoilerControl")
						
##############  Get the params from the database to set up sending alert #######################
############################## Get the From email address ######################################
  from_cursor = db.cursor ()
  from_query = "select * from params_b where Param_Name = 'FromEmail'"
  try:
     from_cursor.execute(from_query)
  except MySQLdb.Error as err:
     print ("******* Error reading FromEmail : ERROR : {}".format(err))
     write_log ('Get FromEmail',err)

  numrows = int (from_cursor.rowcount)
  if numrows == 1:
    Fromres = from_cursor.fetchone()
    FromEmail = Fromres[1]
  else:
    critical_error('Get FromEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param FromEmail  ***"
    return

############################## Get the Support email address ###################################
  support_cursor = db.cursor ()
  support_query = "select * from params_b where Param_Name = 'SupportEmail'"
  try:
     support_cursor.execute(support_query)
  except MySQLdb.Error as err:
     print ("******* Error reading SupportEmail : ERROR : {}".format(err))
     write_log ('Get SupportEmail',err)

  numrows = int (support_cursor.rowcount)
  if numrows == 1:
    Suppres = support_cursor.fetchone()
    SupportEmail = Suppres[1]
  else:
    critical_error('Get SupportEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param SupportEmail  ***"
    return
    
############################## Get the To email address ###################################
  to_cursor = db.cursor ()
  to_query = "select * from params_b where Param_Name = 'ToEmail'"
  try:
     to_cursor.execute(to_query)
  except MySQLdb.Error as err:
     print ("******* Error reading ToEmail : ERROR : {}".format(err))
     write_log ('Get ToEmail',err)

  numrows = int (to_cursor.rowcount)
  if numrows == 1:
    Tores = to_cursor.fetchone()
    ToEmail = Tores[1]
  else:
    critical_error('Get ToEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param ToEmail  ***"
    return

############################## Get the To SystemID ###################################
  SID_cursor = db.cursor () 
  SID_query = "select * from params_b where Param_Name = 'SystemID'"
  try:
     SID_cursor.execute(SID_query)
  except MySQLdb.Error as err:
     print ("******* Error reading SystemID : ERROR : {}".format(err))
     write_log ('Get SystemID',err)

  numrows = int (SID_cursor.rowcount)
  if numrows == 1:
    SIDres = SID_cursor.fetchone()
    SystemID = SIDres[1]
  else:
    critical_error('Get SysID', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param SystemID  ***"
    return
	
	
	
############################## Get the From SMTP address ###################################
  SMTP_cursor = db.cursor ()
  SMTP_query = "select * from params_b where Param_Name = 'ServerSMTP'"
  try:
     SMTP_cursor.execute(SMTP_query)
  except MySQLdb.Error as err:
     print ("******* Error reading ServerSMTP : ERROR : {}".format(err))
     write_log ('Get ServerSMTP',err)

  numrows = int (SMTP_cursor.rowcount)
  if numrows == 1:
    SMTPres = SMTP_cursor.fetchone()
    SMTPParam = SMTPres[1]
  else:
    critical_error('Get ServerSMTP', 'ERROR : Missing', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param SMTPServer  ***"
    return
  

############################## Get the Password  ###################################
  pwd_cursor = db.cursor ()
  pwd_query = "select * from params_b where Param_Name = 'EmailPwd'"
  try:
     pwd_cursor.execute(pwd_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Email Password : ERROR : {}".format(err))
     write_log ('Get EmailPwd',err)

  numrows = int (pwd_cursor.rowcount)
  if numrows == 1:
    Passres = pwd_cursor.fetchone()
    password = Passres[1]
  else:
    critical_error('Get Email Password', 'ERROR : Missing', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param EmailPwd  ***"
    return
  global sendok
  sendok = True

  msg = 'Subject: %s: %s\n\n%s' %(subject, SystemID, msgbody)
  
  try:
     SMTPServer = smtplib.SMTP(SMTPParam)
  except:
     sendok = False
     write_log('SendIP - sending Alert', 'Error Setting SMTP Server - check internet')

  if sendok:
    try:
      SMTPServer.starttls()
    except:
      sendok = False
      write_log('SendIP - sending Alert', 'Error Setting SMTP starttls - check internet')   

  if sendok:
    try:
      SMTPServer.login(FromEmail, password) 
    except:
      sendok = False
      write_log('SendIP - sending Alert', 'Error Setting SMTP login - check internet')   

  if sendok:
    toadrs = [ToEmail] + [SupportEmail]

    try:
      SMTPServer.sendmail(FromEmail, toadrs, msg)
    except:
      sendok = False
      write_log('SendIP - sending Alert', 'Error Setting SMTP sendmail - check internet')   

  if sendok:
    try:
      SMTPServer.quit()
    except:
      sendok = False
      write_log('SendIP - sending Alert', 'Error SMTPServer quit sendmail - check internet')   
  db.close()

  
  
  

# get current datetime
now = datetime.datetime.now()
print "Its %s" % now

sleep (30)
#####################################################################################################
# first get the old IP from the params table:
dbpass = getpass()


db = MySQLdb.connect (host   = "localhost",
                      user   = "TCROOT9000",
                      passwd = dbpass,
                      db     = "BoilerControl")

oldExtip_cursor = db.cursor ()
oldExtip_query = "select * from params_b where Param_Name = 'Ext_IP'"
try:
   oldExtip_cursor.execute(oldExtip_query)
except MySQLdb.Error as err:
   print ("******* Error reading Ext_IP : ERROR : {}".format(err))
   write_log ('Get Ext_IP Param',err)

numrows = int (oldExtip_cursor.rowcount)

if numrows == 1:
  oldExtipres = oldExtip_cursor.fetchone()
  OldEIP = oldExtipres[1]
else:
  critical_error('Get Ext_IP', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
  print "***  Error:  Missing Param Ext_IP  ***"

# thanks to the clever chap who wrote this function, its cool, i got it from github
NewEIP = ipgetter.myip()
NewIIP = get_ip_address('eth0')  


print NewEIP
print NewIIP
  
#####################################################################################################
# next  get the old Internal IP from the params table:

oldIntip_cursor = db.cursor ()
oldIntip_query = "select * from params_b where Param_Name = 'Int_IP'"
try:
   oldIntip_cursor.execute(oldIntip_query)
except MySQLdb.Error as err:
   print ("******* Error reading Int_IP : ERROR : {}".format(err))
   write_log ('Get Int_IP Param',err)

numrows = int (oldIntip_cursor.rowcount)

if numrows == 1:
  oldIntipres = oldIntip_cursor.fetchone()
  OldIIP = oldIntipres[1]
else:
  critical_error('Get Int_IP', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
  print "***  Error:  Missing Param Int_IP  ***"


if (OldEIP <> NewEIP) or (OldIIP <> NewIIP):
  subject = 'TotalControl9000 - IP change notification Email'

  
  os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
  with open('tunnels.json') as data_file:
      datajson = json.load(data_file)

  for i in datajson['tunnels']:
    ngmsg = i['public_url'] + '\n'

  

#use the ipgetter code we imported to get the machines external IP Address
  body = "Your external IP address is currently : " + NewEIP + "  \nYour old external IP was : " + OldEIP \
         + "\nYour internal IP address is currently : " + NewIIP + "\nYour old interal IP address was : " + OldIIP \
         + "\nYour Alexa voice control endpoint address is : " + ngmsg 
		 
# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list


  log_text = "New IP address detected : " + NewEIP
  write_log ('Send IP', log_text)


# if the router is slow to start up the email send can fail, so we need
# to try a few times with a short delay.  if eventually it doesnt work, lets not lose any sleep, just
# write to the log and carry on.					  
  global sendok
  sendok = False
  sendcounter = 0
  while sendcounter < 10:
    sendcounter += 1				  
    send_alert(subject,body)

    if sendok:
      sendcounter = 11;  
      write_log('SendIP Main','Starting up ok - email sent')
    else:
      sleep (15)
    
#  if its failed after 10 goes, just write to the log
  if not sendok:
    write_log('SendIP Main','Startup - sending email failed, but continuing anyway') 
    print "SendIP - Email failed" 
  else:
  
  
# prepare a cursor for storing the new External IP

    cursorEIP= db.cursor()
#
#    # Prepare SQL query to UPDATE a record into the database.
    sql_update = """UPDATE params_b set Param_Value = '"""+str(NewEIP)+"""'
                     where Param_Name ='Ext_IP'"""
   				 
    try:
       cursorEIP.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('SendIP Error updating Ext_IP', err)
       db.rollback()  
  
# prepare a cursor for storing the new internal IP  (I know i could combine, but this is easy)
 
    cursorIIP= db.cursor()
#
#    # Prepare SQL query to UPDATE a record into the database.
    sql_update = """UPDATE params_b set Param_Value = '"""+str(NewIIP)+"""'
                     where Param_Name ='Int_IP'"""
   				 
    try:
       cursorIIP.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('SendIP Error updating Int_IP', err)
       db.rollback()    
  
  
# the end