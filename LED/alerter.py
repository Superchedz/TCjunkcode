################################################################################################
#                                       Alerter.py
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program is used to send an email alert to the configured email address.
#  This program receives params in from the call.
#  
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2015-11-27 GLC   Modified to tidy a few parts of the code
################################################################################################

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



################################################################################################
###################### Function to write to the event log table ################################
################################################################################################

def write_log(Log_From, Log_Text):

  db = MySQLdb.connect("localhost","root","pass123","BoilerControl" )
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
################################ Function to send and email ####################################
################################################################################################

def send_alert(subject, msgbody):
  
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

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
     write_log('Alerter - sending Alert', 'Error Setting SMTP Server - check internet')

  if sendok:
    try:
      SMTPServer.starttls()
    except:
      sendok = False
      write_log('Alerter - sending Alert', 'Error Setting SMTP starttls - check internet')   

  if sendok:
    try:
      SMTPServer.login(FromEmail, password) 
    except:
      sendok = False
      write_log('Alerter - sending Alert', 'Error Setting SMTP login - check internet')   

  if sendok:
    toadrs = [ToEmail] + [SupportEmail]

    try:
      SMTPServer.sendmail(FromEmail, toadrs, msg)
    except:
      sendok = False
      write_log('Alerter - sending Alert', 'Error Setting SMTP sendmail - check internet')   

  if sendok:
    try:
      SMTPServer.quit()
    except:
      sendok = False
      write_log('Alerter - sending Alert', 'Error SMTPServer quit sendmail - check internet')   
  db.close()





subject = str(sys.argv[1])
body = str(sys.argv[2])



# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list
sleep (30)

write_log ('Alerter', 'Startup')


# we need to send an email on start up, this is useful to alert the user the process has started up, 
# for instance after a power cut.  if the router is slow to start up the email send can fail, so we need
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
    write_log('Alerter Main','Starting up ok - email sent')
  else:
    sleep (15)
    
#  if its failed after 10 goes, just write to the log
if not sendok:
  write_log('Alerter Main','Startup - sending email failed, but continuing anyway') 
  print "Alerter - Email failed" 
else:
  print "Alerter - Email sent ok - program complete"

# the end