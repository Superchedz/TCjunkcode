################################################################################################
#                                       Checksense.py
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program is a single run through.
#  This program checks that the sensors for active zones are still receiving regular readings.
#  If any have not had a reading for >10 hours it sends an alert.  
#  
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2016-04-02 GLC   Initial Version
#  1.1      2016-04-03 GLC   Added battery spec to email and added debug print switching
#  2.0      2018-12-16 GLC   Modified so that the zone is deactivated to prevent zones being
#                            jammed on when activated and overheating.  Interval dropped to 20mins
################################################################################################


import time 
import sys 
import MySQLdb 
from time import sleep 
import smtplib 
import mimetypes 
import email 
import email.mime.application 
from datetime import timedelta
import datetime
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
print "##########    CheckSense Version 1.1     ############"
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
#  print "***********************************************************"
#  print "*********************  SENDING ALERT  *********************"
#  print "***********************************************************"
  

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
#  print "Sending....Alert %s" % msgbody
  
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
	  
def turn_zone_off(Zone_id, ZoneOnOff):

  zone_off_cursor = db.cursor ()
  zone_off_query = ("""UPDATE zone_b SET Zone_Active_Ind = '%s' where Zone_ID = %d""" % (ZoneOnOff, Zone_id))
  try:
     zone_off_cursor.execute(zone_off_query)
     db.commit()

  except:
     print ("******* Error updating Current_Zone_Active_Ind : ERROR : {}")
     db.rollback()
  zone_off_cursor.close()
  
  logtext = "Zone %d deactivated as no sensor readings." % (Zone_id)
  write_log('Zone Deactivated',logtext)	  
	  
	  
	  
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
      print "*******  ERROR : Loop_DebugMode param is not numeric  *********"
      critical_error('DebugMode Check', 'Debug Param Not Y or N', '--!! Shutting down ^1 !!--')
    else:
      DebugMode = Debug_res[1]
      return DebugMode
  else:
    critical_error('Get Debug', 'ERROR : Missing Debugmode Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Debugmode param  ***"


################################################################################################
################################ Function to shut down program #################################
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

db = MySQLdb.connect (host   = "localhost",
                      user   = "root",
                      passwd = "pass123",
                      db     = "BoilerControl")

#write_log ('CheckSense', 'Startup')

global sendok
sendok = False
sendcounter = 0

now = datetime.datetime.now()

DebugMode = get_debug()

checktime = now

if DebugMode == "Y":
  print "Current time is %s" % (checktime)
checktime = checktime - timedelta(minutes=20)
if DebugMode == "Y":
  print "Lower comparison time is %s" % (checktime)

Zone_cursor = db.cursor()

Zone_cursor.execute("SELECT Zone_ID, Zone_Name, Zone_Last_Temp_Reading_Dtime, Zone_Sensor_Batt_Pcnt \
                                                              FROM zone_b \
                                                             WHERE Zone_Type = 'T' \
                                                               AND Zone_Last_Temp_Reading_Dtime < (NOW() - INTERVAL 20 MINUTE)")
#Zone_cursor.execute("SELECT Zone_ID, Zone_Name, Zone_Last_Temp_Reading_Dtime, Zone_Sensor_Batt_Pcnt \
#                                                              FROM zone_b \
#                                                             WHERE Zone_Active_Ind = 'Y' \
#                                                               AND Zone_Type = 'T' \
#                                                               AND Zone_Last_Temp_Reading_Dtime < (NOW() - INTERVAL 20 MINUTE)")

numrows = int (Zone_cursor.rowcount)
if DebugMode == "Y":
  
  print "SQL to find expired zones returned %d rows" % (numrows)
  
for y in range (numrows):

  Zone_res = Zone_cursor.fetchone()
  if (Zone_res):
    curr_zone_id = Zone_res[0]
    curr_zone_name = Zone_res[1]
    curr_zone_last_reading_dtime = Zone_res[2]
    curr_zone_batt_pcnt	 = Zone_res[3]

# turn the zone off - this is needed as if no sensor readings are coming in, we need to stop heating immediately.
    if DebugMode == "Y":
      print "Detected a zone without recent readings %d" % (curr_zone_id)	      
      print "Turning zone %d - %s OFF" % (curr_zone_id, curr_zone_name)
    turn_zone_off(curr_zone_id, 'N')

# Send an email to inform the user that system needs attention
    if DebugMode == "Y":
      print 'sending alert email'
    subject = "Warning - Zone sensor Fault"
    msgbody = "Zone : " + str(curr_zone_id) + " (" + curr_zone_name + ") has stopped receiving sensor readings.  "\
              "\nLast reading was received at : " + str(curr_zone_last_reading_dtime) + "\nMost recent battery level is " + str(curr_zone_batt_pcnt) + "%. "\
              "\n\nYou should check the battery immediately. " \
              "\n\nThis message is repeated every 20mins until the problem is resolved. " \
              "\nThe zone has been deactivated to prevent overheating, you must renable it manually once the sensor is back online." \
              "\n\n(The battery is a CR2032 3v)"\
              "\n\nAlso try a reboot or call support if problem persists."\
              "\n\nFrom the TotalControl9000 Support team"
    logtext = "Zone %d" % (curr_zone_id)    
    write_log ('Sensor inactive', logtext)
    if DebugMode == "Y":
      print msgbody
    send_alert(subject, msgbody)


db.close()
