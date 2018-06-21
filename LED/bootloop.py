################################################################################################
#                                       Bootloop.py
#                                       ==========
################################################################################################
#  This program is the main part of the TotalControl9000 system.
#  This program is an infinite loop.
#  it loops round, checking for reboot/shutdown requests from the GUI.  This function used to be 
#  within control1.py, but it meant if that program wasn't running the system couldn't be rebooted
#  hence it was split out.
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2018-06-23 GLC   Initial Version
################################################################################################

import time 
import sys 
import MySQLdb 
from time import sleep 
import mimetypes 
import datetime
import fcntl
import struct
import os

################################################################################################

print "" 
print ""
print "" 
print "" 
print "" 
print "" 
print "" 
print "" 
print "#####################################################" 
print "########## Welcome to BoilerControl 9000 ############"
print "##########      Bootloop Version 1.0     ############"
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
################################ Function to get loop interval #################################
################################################################################################

def get_interval():

  interval_cursor = db.cursor ()
  interval_query = "select * from params_b where Param_Name = 'Loop_Intvl'"

  try:
     interval_cursor.execute(interval_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Loop interval : ERROR : {}".format(err))
     write_log ('Get Interval',err)

  numrows = int (interval_cursor.rowcount)
  if numrows == 1:
    Int_res = interval_cursor.fetchone()
    if not Int_res[1].isdigit():
      print ""
      print "*******  ERROR : Loop_Intvl param is not numeric  *********"
      critical_error('Interval Check', 'Loop_Intvl Not Digit', '--!! Shutting down ^1 !!--')
    else:
      Interval = Int_res[1]
#      write_log('Interval Found',Interval)
#      print "The interval param was found : %s" % (Interval)
      return Interval
  else:
    print "***  Error:  Missing Param Loop_Intvl  ***"
    critical_error('Get Interval', 'ERROR : Missing interval', '--!! Shutting down ^2 !!--')

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


	

################################################################################################
############################# Function to get shutdown mode flag ###############################
################################################################################################

def get_shutdown():

  shutdown_cursor = db.cursor ()
  shutdown_query = "select * from params_b where Param_Name = 'Shutdown'"
 
  try:
     shutdown_cursor.execute(shutdown_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Shutdown param : ERROR : {}".format(err))
     write_log ('ERROR: Get Shutdown',err)

  numrows = int (shutdown_cursor.rowcount)
  if numrows == 1:
    Shutdown_res = shutdown_cursor.fetchone()
    if Shutdown_res[1] != "S" and Shutdown_res[1] != "R" and Shutdown_res[1] != "N":
      print ""
      print "*******  ERROR : Shutdown param is not SRN  *********"
      critical_error('Shutdown Check', 'Shutdown Param Not S R or N', '--!! Shutting down ^1 !!--')
	  shutdown_cursor.close()
    else:
      Shutdown = Shutdown_res[1]
	  shutdown_cursor.close()
      return Shutdown
  else:
    critical_error('Get Shutdown', 'ERROR : Missing Shutdown Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Shutdown param  ***"
    shutdown_cursor.close()
	
################################################################################################
################################# Function to get sysstatus  ###################################
################################################################################################


def critical_error(Log_From, Log_Text, shutdownmsg):
  print "***********************************************************"
  print "***************  Raising CRITICAL ERROR  ******************"
  print "***********************************************************"
  
  write_log (Log_From, Log_Text)
  send_alert('Alert: Heating Control - *** CRASH ***',shutdownmsg, WebAddr)
  sys.exit (shutdownmsg)

  
###############################################################################################
###################################### MAIN PROGRAM ###########################################
###############################################################################################

####################### Define database connection now during startup #########################
# quick snooze here to check that the database has started up before we try and connect
# this seems to be necessary when we run this program automatically at reboot


# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list
#sleep (30) removed this sleep as its moved into the cronjob to allow git to work.

db = MySQLdb.connect (host   = "localhost",
                      user   = "root",
                      passwd = "pass123",
                      db     = "BoilerControl")


  
now = time.strftime('%Y-%m-%d %H:%M:%S')
nowt = time.strftime('%H:%M:%S')
DebugMode = get_debug()



############################################################################################
#################################         Main loop        #################################
############################################################################################
  
#OK, we're now ready to run the main process which is infinite - create an infinte loop - 
while True:

# get current datetime and time
  now = datetime.datetime.now()
  nowt = time.strftime('%H:%M:%S')

# ### Get the interval param for the loop delay - need to read it each loop
# ### incase it's changed since last loop

#need to get interval param from the db each loop in case it changes.
  Interval = get_interval()
  
  DebugMode = get_debug()
  if DebugMode == "Y":
    print "##### Debugging flag is set on (Y) - Sending debug info (lots of it) to console."
  
 
# Check the shutdown param
  Shutitdown = get_shutdown()

  if DebugMode == "Y":
    print "##### Shutdown Param was found %s " % Shutitdown
	
  if Shutitdown == "R":
    print "User reboot requested - performing system reboot"
    logtext = "User Restart Initiated"
    write_log('Restart',logtext)
    clear_cursor = db.cursor ()
 
    clear_query = ("""UPDATE params_b SET Param_Value = '%s' where Param_Name = '%s'""" % ("N", "Shutdown"))
    try:
       clear_cursor.execute(clear_query)
       db.commit()
    except:
       print ("******* Error updating Shutdown Param back to N(R): ERROR : {}")

    db.rollback()
    clear_cursor.close()		
    os.system('sudo reboot')
    sys.exit("Stopping Control1 program")

  if Shutitdown == "S": 
    print "User shutdown requested - performing system shutdown"
    logtext = "User Shutdown detected"
    write_log('Shutdown',logtext)
    clear_cursor = db.cursor ()
 
    clear_query = ("""UPDATE params_b SET Param_Value = '%s' where Param_Name = '%s'""" % ("N", "Shutdown"))
    try:
       clear_cursor.execute(clear_query)
       db.commit()
    except:
       print ("******* Error updating Shutdown Param back to N(S): ERROR : {}")

    db.rollback()
    clear_cursor.close()	
    os.system('sudo shutdown now -h')
    sys.exit("Stopping Control1 program")
  sleep (float(Interval))
  db.commit()


write_log('Main','Closing down - shouldnt be doing this really')
db.close()
