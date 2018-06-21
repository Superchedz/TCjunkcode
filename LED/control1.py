################################################################################################
#                                       Control1.py
#                                       ==========
################################################################################################
#  This program is the main part of the TotalControl9000 system.
#  This program is an infinite loop.
#  On startup this program sends and alert email, this is useful to alert the user that the 
#  system has been restarted, possibly as the result of a reboot or powercut.
#  If additional monitoring/debugging info is required, the debug param in the params_b table
#  can be set to on, that forces this program to PRINT lots of additional info to the terminal, 
#  this can either go to the log file (logs/logpt) or a terminal session if run manually.
#  The program loops every x seconds (x is a configurable param set via the GUI)
#  One each loop, the program checks every zone record and checks its status, then checks for
#  any boost or scheduled events.  It uses the zone  type to determine if there should be a 
#  temp sensor in play for that zone.  The code handles hysteresis, the limit settings for that
#  are currently hard coded.
#  
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2015-11-13 GLC   Added logging for significant switching events for heating zones
#                            This is possible as the cleaner process is now available and will 
#                            prevent the logs becoming too large.
#  1.2      2015-11-22 GLC   Added code to handle the internet being down on startup, handle all
#                            errors that occur when sending startup emails.
#  1.3      2016-01-31 GLC   Added function to get local ip address and include in the email.
#  1.4      2016-01-31 GLC   Minor fix to show target temp when turning on sensor zone rather than
#                            the upper temp of the curve.  (it may confuse people)
#                            Also removed the sleep on startup as moved into cron to support git
#  1.5      2016-02-04 GLC   Added version number into the start up email.
#  1.6      2017-07-15 GLC   Added check on shutdown param to see if we should reboot or shutdown
#  1.6.1    2017-17-15 GLC   Reworded start up email to be more pro
#  2.0      2017-10-27 GLC	 Added logic to handle a Y-Plan zone valve system.
#                            Modified code to get the IP correctly for when connected to wifi or
#                            ethernet etc.  Also added external web address to startup email.
#  2.1      2017-12-21 GLC   Minor amendment to log message wording.
#  2.2      2017-12-21 GLC   Added exit into shutdown and restart to prevent errors after it starts	
#  2.3      2018-02-10 GLC   Proper-Gator9000 upgrade.
#                            Added: Support for wired sensors - new zonetype "W" - not complete
#  2.4      2018-02-23 GLC   Removed shutdown and restart functionality as moved to bootloop.py                            
################################################################################################

import RPi.GPIO as GPIO 
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
print "##########         Version 2.4           ############"
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

def send_alert(subject, msgbody, WebAddr):
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

  msg = 'Subject: %s: %s\n\n%s\nYour Web Address is %s' %(subject,SystemID, msgbody, WebAddr)
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
################################ Function to get day of week####################################
################################################################################################

def get_day():

# ### Select from the database to get the day of week - needed for comparison to schedule
  day_cursor = db.cursor()
  day_query = "select ucase(dayname(curdate()))"

  try:
     day_cursor.execute(day_query)

  except MySQLdb.Error as err:
     db.rollback()
     print ("***** Error on log insert: ERROR: {}".format(err))


  Day = day_cursor.fetchone()
  day = Day[0]
  day_cursor.close() 	
  return day

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


	
def get_web():
  global WebAddr
  web_cursor = db.cursor ()
  web_query = "select * from params_b where Param_Name = 'Ext_Web_Address'"
  global WebAddr
  try:
     web_cursor.execute(web_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Ext_Web_Address param : ERROR : {}".format(err))
     write_log ('ERROR: Get Ext_Web_Address',err)

  numrows = int (web_cursor.rowcount)
  if numrows == 1:
    Web_res = web_cursor.fetchone()
    WebAddr = Web_res[1]
    return WebAddr
  else:
    WebAddr = "Not Found"
    return WebAddr
    print "***  Error:  Missing Param Ext_Web_Address param  ***"


################################################################################################
############################### Function to get YPlan mode flag ################################
################################################################################################

def get_yplan():
# we only need to do this once, no one will ever switch to yplan without rebooting so only needed at startup
  yplan_cursor = db.cursor ()
  yplan_query = "select * from params_b where Param_Name = 'YPlan_YN'"
  global YPlanMode

  try:
     yplan_cursor.execute(yplan_query)
  except MySQLdb.Error as err:
     print ("******* Error reading YPlan_YN param : ERROR : {}".format(err))
     write_log ('ERROR: Get YPlan_YN',err)

  numrows = int (yplan_cursor.rowcount)
  if numrows == 1:
    YPlan_res = yplan_cursor.fetchone()
    if YPlan_res[1] != "Y" and YPlan_res[1] != "N":
      print "*******  Warning : YPlan param is not Y or N - defaulting to N *********"
      print ""
      YPlanMode = "N";
      return YPlanMode
    else:
      YPlanMode = YPlan_res[1] 
      return YPlanMode
  else:
#  again lets not get stressed about it, if the param isn't there just default to N, its only added by the gui anyway
    print "***  Warning:  Missing Param YPlan_YN param   - defaulting to OFF ***"
    YPlanMode = "N";
    return YPlanMode
	
	
	
	
################################################################################################
############################### Function to get YPlan CH zone   ################################
################################################################################################

def get_yplan_ch_zone():
# we only need to do this once, no one will ever switch to yplan without rebooting so only needed at startup
  yplan_ch_cursor = db.cursor ()
  yplan_ch_query = "select * from params_b where Param_Name = 'YPlan_CH_Zone'"
  global YPlanCH

  try:
     yplan_ch_cursor.execute(yplan_ch_query)
  except MySQLdb.Error as err:
     print ("******* Error reading YPlan_CH_Zone param : ERROR : {}".format(err))
     write_log ('ERROR: Get YPlan_CH_Zone',err)
 
  numrows = int (yplan_ch_cursor.rowcount)	 	 
  if numrows == 1:
    YPlan_ch_res = yplan_ch_cursor.fetchone()
    if not YPlan_ch_res[1].isdigit():
      print ""
      print "*******  ERROR : YPlan CH Zone param is not numeric  *********"
      critical_error('YPlan CH Zone Check', 'YPlan CH Zone Not Digit', '--!! Shutting down ^1 !!--')
    else:
      YPlanCH = YPlan_ch_res[1]
      print "##### YPlanCH Param was found value: %s " % YPlanCH	 
      return YPlanCH
  else:
    print "***  Error:  Missing Param YPlan CH Zone   - Y-PLAN Mode is ON so this should exist ***"	 
    critical_error('Get YPlan CH Zone', 'ERROR : Missing param', '--!! Shutting down ^2 !!--')

	 

################################################################################################
############################### Function to get YPlan HW zone   ################################
################################################################################################

def get_yplan_hw_zone():
# we only need to do this once, no one will ever switch to yplan without rebooting so only needed at startup
  yplan_hw_cursor = db.cursor ()
  yplan_hw_query = "select * from params_b where Param_Name = 'YPlan_HW_Zone'"
  global YPlanHW

  try:
     yplan_hw_cursor.execute(yplan_hw_query)
  except MySQLdb.Error as err:
     print ("******* Error reading YPlan_HW_Zone param : ERROR : {}".format(err))
     write_log ('ERROR: Get YPlan_HW_Zone',err)
	 
  numrows = int (yplan_hw_cursor.rowcount)	 	 
  if numrows == 1:
    YPlan_hw_res = yplan_hw_cursor.fetchone()
    if not YPlan_hw_res[1].isdigit():
      print ""
      print "*******  ERROR : YPlan HW Zone param is not numeric  *********"
      critical_error('YPlan HW Zone Check', 'YPlan HW Zone Not Digit', '--!! Shutting down ^1 !!--')
    else:
      YPlanHW = YPlan_hw_res[1]
      print "##### YPlanHW Param was found value: %s " % YPlanHW	 
      return YPlanHW
  else:
    print "***  Error:  Missing Param YPlan HW Zone  - Y-PLAN Mode is ON so this should exist ***"	 
    critical_error('Get YPlan HW Zone', 'ERROR : Missing param', '--!! Shutting down ^2 !!--')


################################################################################################
############################### Function to get YPlan GPIO ID   ################################
################################################################################################

def get_yplan_gpio_zone():
# we only need to do this once, no one will ever switch to yplan without rebooting so only needed at startup
  yplan_gpio_cursor = db.cursor ()
  yplan_gpio_query = "select * from params_b where Param_Name = 'YPlan_GPIO'"
  global YPlanGPIO

  try:
     yplan_gpio_cursor.execute(yplan_gpio_query)
  except MySQLdb.Error as err:
     print ("******* Error reading YPlan_GPIO_Zone param : ERROR : {}".format(err))
     write_log ('ERROR: Get YPlan_GPIO_Zone',err)
	 
  numrows = int (yplan_gpio_cursor.rowcount)	 	 
  if numrows == 1:
    YPlan_gpio_res = yplan_gpio_cursor.fetchone()
    if not YPlan_gpio_res[1].isdigit():
      print ""
      print "*******  ERROR : YPlan GPIO Zone param is not numeric  *********"
      critical_error('YPlan GPIO Zone Check', 'YPlan GPIO Zone Not Digit', '--!! Shutting down ^1 !!--')
    else:
      YPlanGPIO = YPlan_gpio_res[1]
      print "##### YPlanGPIO Param was found value: %s " % YPlanGPIO	 
      return YPlanGPIO
  else:
    print "***  Error:  Missing Param YPlan GPIO Zone  - Y-PLAN Mode is ON so this should exist  ***"	 
    critical_error('Get YPlan GPIO Zone', 'ERROR : Missing param', '--!! Shutting down ^2 !!--')






################################################################################################
################################# Function to get sysstatus  ###################################
################################################################################################

def get_sysstatus():

  sysstatus_cursor = db.cursor ()
  sysstatus_query = "select * from params_b where Param_Name = 'sysstatus'"

  try:
     sysstatus_cursor.execute(sysstatus_query)
  except MySQLdb.Error as err:
     print ("******* Error reading sysstatus : ERROR : {}".format(err))
     write_log ('Error: Get sysstatus',err)

  numrows = int (sysstatus_cursor.rowcount)
  sys_res = sysstatus_cursor.fetchone()
  if numrows == 1:
    sysstatus = sys_res[1]
#    write_log('sysstatus Found',sysstatus)
#    print "The sysstatus param was found : %s" % (sysstatus)
    return sysstatus
  else:
    critical_error('Get sysstatus', 'ERROR : Missing sysstatus', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param sysstatus  ***"

################################################################################################
############################### Function to set zone graphic ###################################
################################################################################################

def set_zone_graphic(Zone_id, ZoneOnOff):

  graphic_cursor = db.cursor ()
  graphic_query = ("""UPDATE zone_b SET Zone_Current_State_Ind = '%s' where Zone_ID = %d""" % (ZoneOnOff, Zone_id))
  try:
     graphic_cursor.execute(graphic_query)
     db.commit()

  except:
     print ("******* Error updating Current_Zone_State_Ind : ERROR : {}")
#    write_log ('Update Curr Zone ind')
     db.rollback()
  graphic_cursor.close()

################################################################################################
################################ Function to shut down program #################################
################################################################################################

def critical_error(Log_From, Log_Text, shutdownmsg):
  print "***********************************************************"
  print "***************  Raising CRITICAL ERROR  ******************"
  print "***********************************************************"
  
  write_log (Log_From, Log_Text)
  send_alert('Alert: Heating Control - *** CRASH ***',shutdownmsg, WebAddr)
  sys.exit (shutdownmsg)

################################################################################################
################################ Function to turn a zone off ###################################
################################################################################################

def turn_off_zone(zone_id, zone_pin):
 
  if DebugMode == "Y":
    print "Inside function to turn a zone %d off pin = %d" % (zone_id, zone_pin)
  GPIO.output(int(zone_pin), 1)
  set_zone_graphic(zone_id, "OFF")

 
  
def check_temp(zone_id, zone_pin, zone_temp, target_temp, curr_zone_state):

  global YPlan_CH_IS_ON
  global YPlan_HW_IS_ON
  if DebugMode == "Y":
    print "Inside function to check zone %d on pin id =  %d temp is %.2f target temp is %.2f" % (zone_id, zone_pin, curr_zone_temp, target_temp)
  
# before we turn a zone on, we need to check the temperature.

# we need to handle a hysteresis curve to avoid turning on and off repeatedly.
  Temp_Upper = float(target_temp) + 0.3
  Temp_Lower = float(target_temp) - 0.3
  if DebugMode == "Y":
    print"Temp check - current temp is %.2f, upper is %.2f and lower is %.2f" % (curr_zone_temp, Temp_Upper, Temp_Lower) 

  if curr_zone_state == "ON":
# we need to check if the zone being turned on is a YPLAN zone and if so, set the flags. 

    if YPlanMode == "Y": 
      if int(zone_id) == int(YPlanCH):
        if DebugMode == "Y":
          print "Yplan is on, CH is on, Setting CH ON flag to True";
        YPlan_CH_IS_ON = True;
      if int(zone_id) == int(YPlanHW):
        if DebugMode == "Y":
          print "Yplan is on, HW is on, Setting HW ON flag to True";       
        YPlan_HW_IS_ON = True;

    if curr_zone_temp >= Temp_Upper:
      if DebugMode == "Y":
        print "Turning zone off as target temp reached"
      turn_off_zone(zone_id, zone_pin)
      logtext = "Zone %d current %.2f new lower target is %.2f" % (zone_id, curr_zone_temp, Temp_Lower)
      write_log('Zone Above Target',logtext)
  else:
    if curr_zone_temp <= target_temp:
      if DebugMode == "Y":
        print "Turning zone on as temp is below target"
      turn_on_zone(zone_id, zone_pin)
      logtext = "Zone %d current %.2f upper target is %.2f" % (zone_id, curr_zone_temp, Temp_Upper)
      write_log('Zone Below Target',logtext)
   

def turn_on_zone(zone_id, zone_pin):
  global YPlan_CH_IS_ON
  global YPlan_HW_IS_ON
  
  if DebugMode == "Y":
    print "Inside function to turn zone %d on pin id =  %d" % (zone_id, zone_pin)
  
  GPIO.output(int(zone_pin), 0)
  set_zone_graphic(zone_id, "ON")
  
 # we need to check if the zone being turned on is a YPLAN zone and if so, set the flags. 
  if YPlanMode == "Y": 
    if int(zone_id) == int(YPlanCH):
      YPlan_CH_IS_ON = True;
    if int(zone_id) == int(YPlanHW):
      YPlan_HW_IS_ON = True;

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
###############################################################################################
###################################### MAIN PROGRAM ###########################################
###############################################################################################
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


# we need to send an email on start up, this is useful to alert the user the process has started up, 
# for instance after a power cut or a reboot.  If the router is slow to start up the email send can fail, so we need
# to try a few times with a short delay.  if eventually it doesnt work, lets not lose any sleep, just
# write to the log and carry on.					  

#write_log ('Control1', 'Startup')

global sendok
global YPlan_CH_IS_ON
global YPlan_HW_IS_ON
	
sendok = False
sendcounter = 0
WebAddr = get_web()

ipaddress = get_ip_address()
print ipaddress
while sendcounter < 10:
  sendcounter += 1				  
  send_alert('TC9000 Alert: Primary switching process (v2.2)- STARTUP: System ID ','Process start successful.  Your local IP is %s' % str(ipaddress), WebAddr)
  if sendok:
    sendcounter = 11;  
    write_log('Control1 - Main','Starting up ok - email sent')
    print "Send ok"
  else:
    print "Control1 - Email error - sleeping for 15 seconds before retrying"
    sleep (15)
    
#  sending the email is not essential so if it failed after 10 goes, lets continue anyway
if not sendok:
  write_log('Control Main','Startup - sending email failed, but continuing anyway') 
  print "The email failed to send, but running main program anyway"	
else:
  print "Control 1 - Email Sent ok - start up complete"
  
now = time.strftime('%Y-%m-%d %H:%M:%S')
nowt = time.strftime('%H:%M:%S')
DebugMode = get_debug()


###########################################################################
# initialise each GPIO pin based on the values stored in the Zone_b table #
###########################################################################

GPIO.setmode(GPIO.BCM)

Zone_cursor = db.cursor()
Zone_cursor.execute("SELECT Zone_ID, PI_Pin_num from zone_b")
numrows = int (Zone_cursor.rowcount)

if DebugMode == "Y":
  print "##### %d Zone records found on Zone_B table " % (numrows)
# loop round for each zone found in the table
for y in range (numrows): 
  Zone_res = Zone_cursor.fetchone()
  if (Zone_res):
    if DebugMode == "Y":
      print "Initialising Zone %d - pin %d" % (Zone_res[0], Zone_res[1]) 
      
    initialise_zone_id = Zone_res[0]
    initialise_zone_pin = int (Zone_res[1])
    GPIO.setup(initialise_zone_pin, GPIO.OUT)

Interval = 60
YPlanMode = get_yplan()
if YPlanMode == "Y":
  print "System is set to YPLAN mode, so getting other params";
  YPlanCH = get_yplan_ch_zone()
  YPlanHW = get_yplan_hw_zone()
  YPlanGPIO = int(get_yplan_gpio_zone())
  
#######  We also need to additionally initialise the GPIO pin used for the YPlan HW-Off config
#######  as this is not set up in a specific zone record - its from the params table

  GPIO.setup(YPlanGPIO, GPIO.OUT)

  
  
  
############################################################################################
#################################         Main loop        #################################
############################################################################################
############################################################################################
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
 
# check is the main system switch has been turned off - if so, skip all processing and just make sure all zones are off.
  Sysstatus = get_sysstatus()


 
#  Get day of week using function, again in case its changed
  day = get_day()

# reset the YPlan flags so we only need to set them to true later on if the zone is turned on.  
  if YPlanMode == "Y": 
    YPlan_CH_IS_ON = False;
    YPlan_HW_IS_ON = False;	
	
# Get all zones from Zones_B table
  Zone_cursor = db.cursor()
  Zone_cursor.execute("SELECT * from zone_b")
  numrows = int (Zone_cursor.rowcount)
  if DebugMode == "Y":
    print "##### %d Zone records found on Zone_B table " % (numrows)

  # loop round for each zone found in the table
  for y in range (numrows):
  
#    print ""
    Zone_res = Zone_cursor.fetchone()
    if (Zone_res):
      if DebugMode == "Y":
        print "Zone found: %d %s %s %s %s %s %s %d %s %s" % (Zone_res[0], Zone_res[1], Zone_res[2], Zone_res[3],Zone_res[4], Zone_res[5], Zone_res[6], Zone_res[7],Zone_res[8], Zone_res[9]) 
      
      curr_zone_id = Zone_res[0]
      curr_zone_name = Zone_res[1]
      curr_zone_active = Zone_res[2]
      curr_zone_state = Zone_res[3]  
      curr_zone_temp = Zone_res[4]
      curr_zone_dtime = Zone_res[5]
      curr_zone_sensor = Zone_res[6]
      curr_zone_offset = Zone_res[7]
      curr_zone_pin = Zone_res[8]
      curr_zone_type = Zone_res[9]

#  first lets add the zone setting offset onto the temp reading
      curr_zone_temp = curr_zone_temp + curr_zone_offset
      
#  we found a configured zone, but lets check if its active, if not set it off.  
#  we need to do this here rather than in the sql so we can pick up zones that have been turned off dynamically.

      if curr_zone_active == "N" or Sysstatus == 'false':
        if curr_zone_state == "ON":
          logtext = "Zone %d turned off due to zone deactivation" % (curr_zone_id)
          write_log('Zone Switch off',logtext)
        turn_off_zone(curr_zone_id, curr_zone_pin)    
      else:

#  zone is active so lets see if it should be on or off depending on the schedule or overrides set up....

# first check for an override record - if there is one, it takes priority over the schedule anyway
         Override_cursor = db.cursor()

#      try:
         Override_cursor.execute("SELECT * from override_b where Zone_id  = %s and Override_start < NOW() and Override_end > NOW()",  (curr_zone_id))
#      except MySQLdb.Error as err:

#      print ("******* Error looking for Override_B : ERROR : {}".format(err))
#      write_log ('Check for Override ',err)

         numrows = int (Override_cursor.rowcount)
         if numrows > 0:
           Over_res = Override_cursor.fetchone()
           if DebugMode == "Y":
             print "Override row found Zone: %s Starttime :%s Endtime: %s Duration: %d Temp: %d" % (Over_res[0], Over_res[1], Over_res[2], Over_res[3], Over_res[4])
           target_temp = Over_res[4]
       
#  we have an active override/boost!!!!
#  it doesn't matter if we find more than 1...put the zone on.
#     we have the latest temp reading from the zone cursor (written by other process PROTOSEN)
#     compare the temps 
#######  call function to turn on zone, set the status in DB
#     but first check if the zone has no temp, it could be hot water, a light or a pump...Woot Woot Go TotalControl9000!!!
#     Stick that up your arse Nest and Hive


# checking if the zone type = "T" is suitable for both wired and wireless sensors as its just the latest temperature reading
# for the zone
           if curr_zone_type == "T":  
             if DebugMode == "Y":
               print "Override with a sensor:check_temp"
             check_temp(curr_zone_id, curr_zone_pin, curr_zone_temp, target_temp, curr_zone_state)
           else:  
             if DebugMode == "Y":
               print "Override for zone with no sensor: so just turn on"
             turn_on_zone(curr_zone_id, curr_zone_pin)
 
             if curr_zone_state == "OFF":
               logtext = "Zone %d switched on due to boost or override1" % (curr_zone_id)
               write_log('Zone Switch on',logtext)
         else:
# no override, so lets see if the schedule is on.
           if numrows == 0:
              if DebugMode == "Y":
                print "No override on zone %d, so lets try and find a schedule row" % (Zone_res[0])
              schedule_cursor = db.cursor()
              try:
                schedule_cursor.execute("SELECT * from schedule_b where Schedule_Day = %s and Schedule_Zone_ID = %s and Schedule_Starttime < %s and Schedule_Endtime >= %s", (day, curr_zone_id, nowt, nowt))

              except MySQLdb.Error as err:
                db.rollback()

              schedule_res = schedule_cursor.fetchone()
              if (schedule_res):
                if DebugMode == "Y":
                  print "schedule found - res = %d %s %s %s %d" % (schedule_res[0], schedule_res[1], schedule_res[2], schedule_res[3], schedule_res[4])
                target_temp = schedule_res[4]
                if curr_zone_type == "T":
                  if DebugMode == "Y":
                    print "++ This zone has a sensor so checking temp"
                  check_temp(curr_zone_id, curr_zone_pin, curr_zone_temp, target_temp, curr_zone_state)  
                else:
                  if DebugMode == "Y":
                    print "++ This zone does not have a sensor so just turn it on"
                  turn_on_zone(curr_zone_id, curr_zone_pin)   
                  if curr_zone_state == "OFF":
                    logtext = "Zone %d turned on due to schedule event" % (curr_zone_id)
                    write_log('Zone Switch on',logtext) 
                  schedule_cursor.close() 	
              else:
#           there was no override and no current schedule, so make sure zone is off.
                if DebugMode == "Y":
                  print "No schedule row found so turning off to make sure its off"

                if curr_zone_state == "ON":
                  logtext = "Zone %d turned off" % (curr_zone_id)
                  write_log('Zone Switch off',logtext)

                turn_off_zone(curr_zone_id, curr_zone_pin)   

# so we've just been through and sorted out all the zones being on and off, but we now need to work out if we need to 
# set the YPlan HW-OFF GPIO pin on or off

  if DebugMode == "Y":
    print "Yplan mode is set to %s" % (YPlanMode)
    if YPlanMode == "Y":
      print "YPlan_CH_IS_ON = %s" % (YPlan_CH_IS_ON)
      print "YPlan_HW_IS_ON = %s" % (YPlan_HW_IS_ON)
 
  if (YPlanMode == "Y"):
    if(YPlan_CH_IS_ON) and (YPlan_HW_IS_ON == False):	
      if DebugMode == "Y":
        print "HW zone is OFF and CH zone is ON so set HW-OFF to be on"
      GPIO.output(int(YPlanGPIO), 0)
    else:
      if DebugMode == "Y":
        print "Turning HW-OFF to off as either neither, both or just HW are on"
      GPIO.output(int(YPlanGPIO), 1)
  sleep (float(Interval))
  Zone_cursor.close()

write_log('Main','Closing down - shouldnt be doing this really')
db.close()
