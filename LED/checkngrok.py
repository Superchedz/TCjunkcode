###############################################################################################
################################################################################################
#                                       Checkngrok.py
#                                       ==========
################################################################################################
#  This program is the main part of the TotalControl9000 system.
#  
#  It is run regularly via Cron to check the status of the NGROK process and check for any
#  changes to its address, if any is found it emails the new address to allow the AWS console 
#  to be updated.
##################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2019-02-15 GLC   Initial Version
###################################################################################################

import time 
import sys 
import MySQLdb 
from time import sleep 
import smtplib 
import mimetypes 
import email 
import email.mime.application 
import datetime
import socket
import fcntl
import struct
import os
import json
from getpw import getpass
################################################################################################


print "" 
print "#####################################################" 
print "########## Welcome to BoilerControl 9000 ############"
print "##########       Checkngrok v1.0         ############"
print "#####################################################" 
print ""

################################################################################################
###################### Function to write to the event log table ################################
################################################################################################

def write_log(Log_From, Log_Text):
#  print "************** Creating log***************"
  log_cursor = db.cursor()
 
  sql = """INSERT INTO log(Log_From, Log_Text) VALUES ('"""+Log_From+"""','"""+Log_Text+"""')""" 

  try:
     log_cursor.execute(sql)
     db.commit()

  except MySQLdb.Error as err:
     db.rollback()
     print ("***** Error on log insert: ERROR: {}".format(err))

  log_cursor.close() 	

################################################################################################
################################ Function to send and email ####################################
################################################################################################

def send_alert(subject, msgbody):
  print "***********************************************************"
  print "*********************  SENDING ALERT  *********************"
  print "***********************************************************"
 

##############  Get the params from the database to set up sending alert #######################
############################## Get the From email address ###################################
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

  msg = 'Subject: %s: %s\n\n%s' %(subject,SystemID, msgbody)
  print "Sending....Alert %s" % msgbody
  
  try:
     SMTPServer = smtplib.SMTP(SMTPParam)
  except:
     sendok = False
     write_log('Protosen - sending Alert', 'Error Setting SMTP Server - check internet')


  if sendok:
    try:
      SMTPServer.starttls()
    except:
      sendok = False
      write_log('Protosen - sending Alert', 'Error Setting SMTP starttls - check internet')   

  if sendok:
    try:
      SMTPServer.login(FromEmail, password) 
    except:
      sendok = False
      write_log('Protosen - sending Alert', 'Error Setting SMTP login - check internet')   


  if sendok:
    toadrs = [ToEmail] + [SupportEmail]
    try:
      SMTPServer.sendmail(FromEmail, toadrs, msg)
    except:
      sendok = False
      write_log('Protosen - sending Alert', 'Error Setting SMTP sendmail - check internet')   
  if sendok:
    try:
      SMTPServer.quit()
    except:
      sendok = False
      write_log('Protosen - sending Alert', 'Error SMTPServerquit - check internet')     
	  

################################################################################################
############################### Function to get Alexa mode flag ################################
################################################################################################

def get_Alexa():

  alexa_cursor = db.cursor ()
  alexa_query = "select * from params_b where Param_Name = 'Alexa_YN'"
  global Alexa_ON
  try:
     alexa_cursor.execute(alexa_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Alexa param : ERROR : {}".format(err))
     write_log ('ERROR: Get Alexa_YN',err)

  numrows = int (alexa_cursor.rowcount)
  if numrows == 1:
    Alexa_res = alexa_cursor.fetchone()
    if Alexa_res[1] != "Y" and Alexa_res[1] != "N":
      print ""
      print "*******  ERROR : Alexa param is not Y or N  *********"
      critical_error('Alexa Check', 'Alexa Param Not Y or N', '--!! Shutting down ^1 !!--')
    else:
      AlexaON = Alexa_res[1]
      return AlexaON
  else:
    print "***  Error:  Missing Param Alexa param  ***"
    critical_error('Get Alexa', 'ERROR : Missing Alexa Param', '--!! Shutting down ^2 !!--')

	
def get_curr_ngrok():
  global currNGROK
  ng_cursor = db.cursor ()
  ng_query = "select * from params_b where Param_Name = 'NGROK_address'"

  try:
     ng_cursor.execute(ng_query)
  except MySQLdb.Error as err:
     print ("******* Error reading NGROK_adress param : ERROR : {}".format(err))
     write_log ('ERROR: Get NGROK_address',err)

  numrows = int (ng_cursor.rowcount)
  
  if numrows == 1:
    ng_res = ng_cursor.fetchone()
    currNGROK = ng_res[1]
    return currNGROK
  else:
    currNGROK = "Not Found"
    return currNGROK
    print "***  Error:  Missing Param NGROK_address param  ***"


################################################################################################
############################### Function to get debug mode flag ################################
################################################################################################

def get_debug():

  debug_cursor = db.cursor ()
  debug_query = "select * from params_b where Param_Name = 'DebugMode'"
  global DebugMode
  try:
     debug_cursor.execute(debug_query)
  except MySQLdb.Error as err:
     print ("******* Error reading DebugMode param : ERROR : {}".format(err))
     write_log ('ERROR: Get DebugMode',err)

  numrows = int (debug_cursor.rowcount)
  if numrows == 1:
    Debug_res = debug_cursor.fetchone()
    if Debug_res[1] != "Y" and Debug_res[1] != "N":
      print ""
      print "*******  ERROR : Loop_DebugMode param is not Y or N  *********"
      critical_error('DebugMode Check', 'Debug Param Not Y or N', '--!! Shutting down ^1 !!--')
    else:
      DebugMode = Debug_res[1]
      return DebugMode
  else:
    print "***  Error:  Missing Param Debugmode param  ***"
    critical_error('Get Debug', 'ERROR : Missing Debugmode Param', '--!! Shutting down ^2 !!--')


##############################################################################################
# function to get the local ip address to be included in the startup email.
##############################################################################################

def get_ip_address():
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.connect(("8.8.8.8", 80))
#    return s.getsockname()[0]
	
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
        # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
    print "ip get routine"
    print IP	  
  except:
    print "error getting ip, defaulting to 127.0.0.1"
    IP = '127.0.0.1'
  finally:
      s.close()
  return IP
    
###############################################################################################
###################################### MAIN PROGRAM ###########################################
###############################################################################################
processing_successful = True
dbpass = getpass()

db = MySQLdb.connect (host   = "localhost",
                      user   = "TCROOT9000",
                      passwd = dbpass,
                      db     = "BoilerControl")

# get the alexa param and check if its on, if so send the ngrok address in the start up email.
# need to check the tunnel is available too.

AlexaON = get_Alexa()

ngmsg = "undefined"
if AlexaON == "Y":
#  ipaddress = get_ip_address()
  DebugMode = get_debug()
  ngmsg = "not detected"
# get the ngrok tunnel details as they need to go in the startup email
  try:
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)
  except:
    processing_successful = False
    print "*** Error - Alexa is set to ON but no endpoint found ***"
    write_log('** Error checkngrok.py','Unable to determine endpoint address found')
    ngmsg = ": ** Alexa endpoint not set **"
  else:
    for i in datajson['tunnels']:
      ngmsg = i['public_url'] + '\n'
  print " "
  print " " 
  print "Current tunnel address : " + ngmsg
  
# check if it's changed since we last updated the database
  if processing_successful == True:
 
    curr_ngrok = get_curr_ngrok()      
    print "Params table value     : " + curr_ngrok
  
    if curr_ngrok != ngmsg:
      print "Not equal, sending email and updating database"
# store the ngrok in the database so its available to the gui

      ngrok_cursor = db.cursor ()
      ngrok_query = ("""UPDATE params_b SET Param_Value = '%s' where Param_Name = 'NGROK_address'""" % (ngmsg))
 
      try:
         ngrok_cursor.execute(ngrok_query)
         db.commit()
      except MySQLdb.Error as err:
         print ("***** Error on save NGROK address to param: ERROR: {}".format(err))
         write_log('Update in checkngrok', err)
         db.rollback()
         processing_successful = False
      ngrok_cursor.close()
     
      if processing_successful == True:    
# format up the alert email with info
        subject = "TC9000 - NGROK endpoint change detected: System ID"
        msgbody = "Dear valued customer,\n\n" \
                  "A change has been detected in your NGROK Alexa Endpoint address \n" \
                  "Your old value was : " + str(curr_ngrok) + "\n" \
                  "Your Alexa end point is now: " + str(ngmsg) + "\n" \
                  "You should update the end point into the AWS console here https://developer.amazon.com/alexa/ \n\n" \
                  "This is probably because your system lost its internet connection for an extended period. \n"\
                  "\n\nFrom \n\n" \
                  "The TotalControl9000 Support Team"
            
        send_alert(subject, msgbody) 
      else:
        send_alert("TC9000 system error", "Error while processing NGROK checks - refer to logs")       
  
    write_log('NGROK Address','Change in address detected, alert sent')
db.close()
