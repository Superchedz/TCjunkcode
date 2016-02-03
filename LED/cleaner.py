################################################################################################
#                                       Cleaner.py
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program runs periodically, normally once per day to purge old temporary records from the
#  database.  It runs via CronTab.
#  It retrieves the retention period param from the params_b table to determine the age of records
#  to delete.
#  If you need to debug the program - set the debug param ON in the database and it will print
#  many additional items of data.
#  It also writes a summary record to the log_b table with the details of the number of records
#  delete.
#
#  Deletes from tables:  zone_temp_hist_b
#                        log_b 
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2015-12-05 GLC   Added deletion of log_b to the program.
#  
################################################################################################
 
import time 
import sys 
import MySQLdb 
from time import sleep 
import smtplib 
import mimetypes 
import email 
import email.mime.application 
import datetime


print "" 
print "#############################################################" 
print "########## Welcome to Boiler Control Log Cleaner ############"
print "#############################################################" 
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
  except MySQLdb.error as err:
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
  except MySQLdb.error as err:
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

############################## Get the From SMTP address ###################################
  SMTP_cursor = db.cursor ()
  SMTP_query = "select * from params_b where Param_Name = 'ServerSMTP'"
  try:
    SMTP_cursor.execute(SMTP_query)
  except MySQLdb.error as err:
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
  except MySQLdb.error as err:
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

	
	
  msg = 'Subject: %s:%s\n\n%s' %(subject, SystemID, msgbody)
  print "Sending....Alert %s" % msgbody
  SMTPServer = smtplib.SMTP(SMTPParam)
  SMTPServer.starttls()
  toadrs = [ToEmail] + [SupportEmail]

  SMTPServer.login(FromEmail, password) 
  SMTPServer.sendmail(FromEmail, toadrs, msg)
  SMTPServer.quit()

def get_debug():

  debug_cursor = db.cursor ()
  debug_query = "select * from params_b where Param_Name = 'DebugMode'"
  global DebugMode
  try:
     debug_cursor.execute(debug_query)
  except MySQLdb.error as err:
     print ("******* Error reading DebugMode param : ERROR : {}".format(err))
     write_log ('Get DebugMode',err)

  numrows = int (debug_cursor.rowcount)
  if numrows == 1:
    Debug_res = debug_cursor.fetchone()
    if Debug_res[1] != "Y" and Debug_res[1] != "N":
      print ""
      print "*******  ERROR : Loop_DebugMode param is not numeric  *********"
      critical_error('DebugMode Check', 'Debug Param Not Y or N', '--!! Shutting down ^1 !!--')
    else:
      DebugMode = Debug_res[1]
      return DebugMode
  else:
    critical_error('Get Debug', 'ERROR : Missing Debugmode Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Debugmode param  ***"

def get_retention():

  retention_cursor = db.cursor ()
  retention_query = "select * from params_b where Param_Name = 'Log_Ret'"
  try:
     retention_cursor.execute(retention_query)
  except MySQLdb.error as err:
     print ("******* Error reading Log Retenton param : ERROR : {}".format(err))
     write_log ('Get Log_Ret',err)

  numrows = int (retention_cursor.rowcount)
  if numrows == 1:
    Ret_res = retention_cursor.fetchone()
    if not Ret_res[1].isdigit():
      print ""
      print "*******  ERROR : Log Res param is not numeric  *********"
      critical_error('Log Ret Check', 'Log_Ret Not Digit', '--!! Shutting down ^1 !!--')
    else:
      LogRet = Ret_res[1]
      return LogRet
  else:
    critical_error('Get Log_Ret', 'ERROR : Missing Log_Ret Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Log_Ret param  ***"
	
	
	
	
################################################################################################
################################# Function to get sysstatus  ###################################
################################################################################################


def critical_error(Log_From, Log_Text, shutdownmsg):
  print "***********************************************************"
  print "***************  Raising CRITICAL ERROR  ******************"
  print "***********************************************************"
  
  write_log (Log_From, Log_Text)
  send_alert('Alert: Heating Control - *** CRASH ***',shutdownmsg)
  sys.exit (shutdownmsg)

###############################################################################################
###############################################################################################
###################################### MAIN PROGRAM ###########################################
###############################################################################################
###############################################################################################

Error_state = False

db = MySQLdb.connect (host   = "localhost",
                      user   = "root",
                      passwd = "pass123",
                      db     = "BoilerControl")

write_log('Log Cleaner','Starting up')
now = time.strftime('%Y-%m-%d %H:%M:%S')
nowt = time.strftime('%H:%M:%S')
DebugMode = get_debug()
Log_Retention_days = int(get_retention())

if DebugMode == "Y":
  print Log_Retention_days

Log_hist_clean = db.cursor()

try:
  Log_hist_clean.execute("DELETE FROM zone_temp_hist_b WHERE log_date < ADDDATE(CURDATE(), -%s)", Log_Retention_days)
except MySQLdb.Error as err:
  print "oh no!!! There was an error deleting from zone_temp_hist_b"
  write_log ('Log Cleaner', '*** ERROR *** Deleting from zone_temp_hist_b')
  send_alert('Log Cleaner Error', '***Error detected deleting from zone_temp_hist_b during scheduled job')
  Error_state = True

if not Error_state:  
  numrows = int (Log_hist_clean.rowcount)
  print "##### %d Temp hist records deleted on zone_temp_hist_b table " % (numrows)
  if DebugMode == "Y":
    print "##### %d Temp hist records deleted on zone_temp_hist_b table " % (numrows)

# ironically lets write to the log 
  write_log('Log Cleaner', 'Deleted %d temp hist records, retention %d days' % (numrows, Log_Retention_days))


if not Error_state:  
  Log_clean = db.cursor()

  try:
    Log_clean.execute("DELETE FROM log WHERE log_time < ADDDATE(CURDATE(), -%s)", Log_Retention_days)
  except MySQLdb.Error as err:
    print "oh no!!! There was an error deleting from the log table"
    write_log ('Log Cleaner', '*** ERROR *** Deleting from log')
    send_alert('Log Cleaner Error', '***Error detected deleting from log during scheduled job')
    Error_state = True

if not Error_state:  
  numrows = int (Log_clean.rowcount)
  print "##### %d Temp hist records deleted on zone_temp_hist_b table " % (numrows)
  if DebugMode == "Y":
    print "##### %d Temp hist records deleted on zone_temp_hist_b table " % (numrows)

# ironically lets write to the log 
  write_log('Log Cleaner', 'Deleted %d log records, retention %d days' % (numrows, Log_Retention_days))
    
db.commit()
db.close()
