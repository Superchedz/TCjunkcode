################################################################################################
#                                       Protosen.py 
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program monitors either the serial or UDP port and reads in the temperature sensor readings.
#  It matches the sensor ID with a zone_id in the database and writes the record to the 
#  zone_temp_hist_b table.  This program is an infinite loop.
#  On startup this program sends and alert email, this is useful to alert the user that the 
#  system has been restarted, possibly as the result of a reboot or powercut.
#  If additional monitoring/debugging info is required, the debug param in the params_b table
#  can be set to on, that forces this program to PRINT lots of additional info to the terminal, 
#  this can either go to the log file (logs/logpt) or a terminal session if run manually.
#  The program also records the sensor battery level readings and writes these to the zone_b
#  table.
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2015-11-22 GLC   Added code to handle the internet being down on startup, handle all
#                            errors that occur when sending startup emails.
#  1.2      2016-01-01 GLC   Modified so that the zone id is derived from the db config rather
#                            than assuming the sensor id matches the zone id.
#  1.3      2016-02-03 GLC   Removed sleep at start as have moved it to cron to support git.
#  1.4      2016-02-04 GLC   Added debug checking to allow for printing of debug info.
#  2.0      2016-02-04 GLC   Added code to support both UDP and Serial comms in single program
#  2.1      2016-02-10 GLC   Removed erroneous print statement within UDP loop
#  3.0      2016-04-02 GLC   Added support for fobs
#  3.1      2017-07-16 GLC   Added sensor id to alert for unconfigured sensor reading received
#  3.1.1    2017-17-15 GCL   Reworded start up email to be more pro
################################################################################################
import serial
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
import socket
#
# SETTINGS
#
# Default settings for program; port, baud rate, temperature threshold, number of readings to store
# set up serial port for temperature readings


# for Serial IO
DEVICE = '/dev/ttyAMA0'
BAUD = 9600
global Code_Version
Code_Version = 'V3.1.1'
 
# for UDP IO
FROM_PORT = 50140
TO_PORT = 50141


# END OF SETTINGS

################################################################################################
###################### Function to write to the event log table ################################
################################################################################################

def write_log(Log_From, Log_Text):
#  print "************** Creating log***************"

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
    print "***  Error:  Missing Param FromEmail  ***"
    critical_error('Get FromEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
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
    print "***  Error:  Missing Param SupportEmail  ***"
    critical_error('Get SupportEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
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
    print "***  Error:  Missing Param ToEmail  ***"
    critical_error('Get ToEmail', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
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
    print "***  Error:  Missing Param SystemID  ***"
    critical_error('Get SysID', 'ERROR : Missing Param', '--!! Shutting down ^2 !!--')
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
    print "***  Error:  Missing Param SMTPServer  ***"
    critical_error('Get ServerSMTP', 'ERROR : Missing param ServerSMTP', '--!! Shutting down ^2 !!--')
    return
  

############################## Get the Email Password  ###################################
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
    print "***  Error:  Missing Param EmailPwd  ***"
    critical_error('Get Email Password', 'ERROR : Missing param EmailPwd', '--!! Shutting down ^2 !!--')
    return
  global sendok
  sendok = True

  msg = 'Subject: %s:%s\n\n%s' %(subject, SystemID, msgbody)
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
      write_log('Protosen - sending Alert', 'Error SMTPServer quit sendmail - check internet')   
  db.close()

def writeTemp(llap_sensor_id, llap_temp):

# we need to make sure the temp is always just 2dp to match the database field 
  zone_id, found_zone_ind = get_zone(llap_sensor_id) 

  if found_zone_ind:             
    if is_number(llap_temp) == True:
      if DebugMode == "Y":
        print "DEBUG: *** TEMP *** in writeTemp function - Sensor id " + llap_sensor_id + " gave temp of " + str(llap_temp)

      temp2dp = float(float(int(float(llap_temp)*100)) / 100)
      now = datetime.datetime.now()
# Open database connection
      db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

# prepare a cursor for storing the temperature reading
      cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
      sql = """INSERT INTO zone_temp_hist_b (log_date,
                                             zone_id,
                                             temperature)
               VALUES ('"""+str(now)+"""','"""+str(zone_id)+"""',"""+str(temp2dp)+""")"""
      try:
          cursor.execute(sql)
          db.commit()
      except:
          db.rollback()
#
#    # prepare a cursor for storing just the current temperature reading against the zone record
      cursor3 = db.cursor()
      if DebugMode == "Y":
        print "DEBUG: temp2dp is " + str(temp2dp)
#    # Prepare SQL query to UPDATE a record into the database.
      sql_update = """UPDATE zone_b set Zone_Last_Temp_Reading = '"""+str(temp2dp)+"""',
                               Zone_Last_Temp_Reading_Dtime = '"""+str(now)+"""'
                       where Zone_ID ='"""+str(zone_id)+"""'"""
      try:
         cursor3.execute(sql_update)
         db.commit()
      except MYSQLdb.Error as err:
         write_log ('ProtoSen Error writing temps', err)
         db.rollback()
      db.close()
    else:
      print "DEBUG: Temp wasn'numeric, oh dear"
      write_log ('ProtoSen Error non-numeric temp', err)
  else:
    print "DEBUG: Zone wasnt found - E554"
    if DebugMode == "Y":
      print "DEBUG: llap_temp" + llap_temp


def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False


def get_zone(sensor_id):

# Open database connection
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )
  if DebugMode == "Y":
    print "DEBUG: Get_zone: about to do zone lookup"
    print "DEBUG: Sensor id for lookup is : " + sensor_id
  zone_cursor = db.cursor ()
  zone_query = ("""select Zone_ID from zone_b where Zone_Sensor_ID = '%s'""" % (sensor_id))

  try:
     zone_cursor.execute(zone_query)
  except MySQLdb.Error as err:
     print ("******* Error reading get_zone : ERROR : {}".format(err))
     write_log ('Get Zone',err)
     critical_error('Scanner Job', 'ERROR : Cursor in getzone', '--!! Shutting down ^2\n Contact Support!!--')

  numrows = int (zone_cursor.rowcount)
  if DebugMode == "Y":
    print "DEBUG: Zone SQL returned " + str(numrows) + " rows" 
  if numrows == 1:
    zone_id_res = zone_cursor.fetchone()
    zone_id = zone_id_res[0]
    zone_found_ind = True
  else:
    zone_id = 0
    zone_found_ind = False
    if numrows > 1:
      if DebugMode == "Y":
        print "***  Error:  Multiple Zones with same sensor id Error  ***"
      critical_error('Scanner Job', 'ERROR : Multiple Zones set for a Sensor', '--!! Shutting down ^2 !!--')
    if numrows == 0:
      if DebugMode == "Y":
        print "***  Warning:  No Zone set for sensor id - Warning ***"
      send_alert('Warning: Scanner Job - *** Warning ***','Sensor reading recieved for unconfigured sensor - check config : Sensor : ' + sensor_id)
      write_log ('Scanner Job: Warning no zone configured for sensor', str(sensor_id))
  return (zone_id, 	zone_found_ind) 
  
  
def get_fob_action(fob_id, button_id):

# Open database connection
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )
  if DebugMode == "Y":
    print "DEBUG: Get_fob action - about to do fob_butt_action_b lookup"
    print "DEBUG: Fob id for lookup is : " + fob_id
    print "DEBUG: Fob button pressed is : " + button_id
  fob_action_cursor = db.cursor ()
  fob_query = ("""select Butt_Zone_ID, Butt_Action_Type, Butt_Boost_mins, Butt_Boost_Temp from fob_butt_action_b where Fob_ID = '%s' and Fob_Butt = '%s'""" % (fob_id, button_id))
  
  if DebugMode == "Y":
    print "DEBUG: " + fob_query 
  
  try:
     fob_action_cursor.execute(fob_query)
  except MySQLdb.Error as err:
     print ("******* Error reading get_fob_action cursor : ERROR : {}".format(err))
     write_log ('Get Fob Act',err)
     critical_error('Scanner Job', 'ERROR : Cursor in getfobaction', '--!! Shutting down ^2\n Contact Support!!--')

  numrows = int (fob_action_cursor.rowcount)
  if DebugMode == "Y":
    print "DEBUG: Zone SQL returned " + str(numrows) + " rows" 
  if numrows == 1:
    fob_action_res = fob_action_cursor.fetchone()
    Butt_Zone_ID = fob_action_res[0]
    Butt_Action_type = fob_action_res[1]
    Butt_Boost_mins = fob_action_res[2]
    Butt_Boost_Temp = fob_action_res[3]
    fob_found_ind = True
    if DebugMode == "Y":
      print "DEBUG: Inside function to process button press: the following was retrieved from the DB"
      print "DEBUG: Button_Zone_ID = " + str(Butt_Zone_ID)
      print "DEBUG: Butt_Action_type = " + Butt_Action_type
      print "DEBUG: Butt_Boost_min = " + str(Butt_Boost_mins)
      print "DEBUG: Butt_Boost_Temp = " + str(Butt_Boost_Temp)

# determine what to do with the button press.  If the zone is off then we insert a boost record as per the config.
# if the zone is already boosted, clear the boost regardless of where it came from.
# we can ignore the schedule and just do the above as it makes no difference, schedule always takes priority

# first check for an active override record
    Override_cursor = db.cursor()

    try:
      Override_cursor.execute("SELECT 1 from override_b where Zone_id  = %s and Override_start < NOW() and Override_end > NOW()",  (Butt_Zone_ID))
    except MySQLdb.Error as err:

      print ("******* Error looking for Override_B (fob): ERROR : {}".format(err))
      write_log ('Check for Override fob error ',err)

    numrows = int (Override_cursor.rowcount)
    if numrows > 0:

      Over_res = Override_cursor.fetchone()
      if DebugMode == "Y":
        print "Override row found for zone when button pressed will delete record now to turn the zone off"
        print Butt_Zone_ID

      Boost_Burner_Cursor = db.cursor()
        
      try:
        Boost_Burner_Cursor.execute("DELETE FROM override_b where Zone_id  = %s and Override_start < NOW() and Override_end > NOW()",  (Butt_Zone_ID))
        db.commit()
      except MySQLdb.Error as err:
        print "oh no!!! There was an error deleting from Override_B for fob pres"
        write_log ('Protosen', '*** ERROR *** Deleting from Override - Fob')
        send_alert('Protosen', '***Error detected deleting from Override_B for fob action')
        Error_state = True
      finally:
        Boost_Burner_Cursor.close()
        db.close()

      if DebugMode == "Y":
        delnumrows = int (Boost_Burner_Cursor.rowcount)
        print delnumrows
    else:

# No active boost to turn zone on
      fob_now = datetime.datetime.now()
      if Butt_Action_type == "B":
        fob_boost_end = now + datetime.timedelta(minutes = Butt_Boost_mins)
      else:
        if DebugMode == "Y":
          print "DEBUG: Boost type is toggle so boosting for 999 minutes and 99 degrees - should not be a temp zone"
        fob_boost_end = now + datetime.timedelta(minutes = 999)
        Butt_Boost_Temp = 99

      cursor = db.cursor()
      
# Prepare SQL query to INSERT a record into the database.
      sql = """INSERT INTO override_b       (Zone_ID,
                                             Override_start,
                                             Override_end,
                                             Override_Duration_Mins,
                                             Override_Temp)
               VALUES ('"""+str(Butt_Zone_ID)+"""','"""+str(fob_now)+"""', '"""+str(fob_boost_end)+"""',  '"""+str(Butt_Boost_mins)+"""', '"""+str(Butt_Boost_Temp)+"""')"""

      if DebugMode == "Y":
        print "DEBUG: SQL to insert the Fob boost is : " + sql
      try:
          cursor.execute(sql)
          db.commit()
      except MySQLdb.Error as err:
          db.rollback()
          if DebugMode == "Y":
            print "DEBUG: oh shoot, error inserting an override record"
            print ("***** Error on Override insert for fob: ERROR: {}".format(err))
  else:
    if numrows > 1:
      if DebugMode == "Y":
        print "***  Error:  Multiple Fob rows with same fob id Error  ***"
        critical_error('Scanner Job', 'ERROR : Multiple Fob Rows set for a Fob ID and button', '--!! Shutting down ^2 !!--')
        if numrows == 0:
          if DebugMode == "Y":
            print "***  Warning:  No Fob found for button push detected for sensor id - Warning ***"

          send_alert('Warning: Scanner Job - *** Warning ***','Button detected for unconfigured fob - check config')
          write_log ('Scanner Job: Warning no fob configured for button press', str(fob_id))

  
################################################################################################
############################### Function to get debug mode flag ################################
################################################################################################

def get_debug():
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )
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
      print "*******  ERROR : DebugMode param is not numeric  *********"
      critical_error('Scanner Job Error', 'Debug Param Not Y or N', 'Debug Param was not valid\n Expected Y or N, found : ' + Debug_res[1] + '\n--!! Shutting down ^1 !!--')
    else:
      DebugMode = Debug_res[1]
      return DebugMode
  else:
    critical_error('Scanner job ERROR', 'ERROR : Missing Debugmode Param', 'Debug Param not found\n--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Debugmode param  ***"

def critical_error(Log_From, Log_Text, shutdownmsg):
  print "***********************************************************"
  print "***************  Raising CRITICAL ERROR  ******************"
  print "***********************************************************"
  
  write_log (Log_From, Log_Text)
  send_alert('Alert: Scanner Job - *** CRASH *** ' + Code_Version + ' ', shutdownmsg)
  sys.exit (shutdownmsg)

  
  
def get_Sensor_Mode():
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )
  sensormode_cursor = db.cursor ()
  sensormode_query = "select * from params_b where Param_Name = 'Sensor_Mode'"
  global SensorMode
  try:
     sensormode_cursor.execute(sensormode_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Sensor_Mode param : ERROR : {}".format(err))
     write_log ('ERROR: Get SensorMode',err)

  numrows = int (sensormode_cursor.rowcount)
  if numrows == 1:
    Sensormode_res = sensormode_cursor.fetchone()
    if Sensormode_res[1] != "SERIAL" and Sensormode_res[1] != "UDP":
      print ""
      print "********  ERROR : SensorMode param is not valid  ********** Value found: " + Sensormode_res[1]
      critical_error('Scanner job', 'SensorMode Param Not SERIAL or UDP', '--!! Shutting down ^1 !!--\n Error: Sensor Mode param not valid: ' + Sensormode_res[1])
    else:
      SensorMode = Sensormode_res[1]
      return SensorMode
  else:
    critical_error('Scanner Job', 'ERROR : Missing SensorMode Param', '--!! Sensor_Mode param Error - Shutting down ^2 !!--\nContact Support')



def writeBatt(zone_id, battpct):

#    now = datetime.datetime.now()
# Open database connection
    db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

# prepare a cursor for storing the temperature reading
    cursor = db.cursor()

#
#    # prepare a cursor for storing just the current temperature reading against the zone record
    cursorb = db.cursor()
#
#    # Prepare SQL query to UPDATE a record into the database.
    sql_update = """UPDATE zone_b set Zone_Sensor_Batt_Pcnt = '"""+str(battpct)+"""'
                     where Zone_ID ='"""+zone_id+"""'"""
    try:
       cursorb.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('Scanner Job Error writing Battery percent', err)
       db.rollback()
#

def update_fob_batt(Fob_ID, battpct):
###############################################################################################
################## Function to write the battery level of a fob to the database ###############
###################### Fobs send a battery level reading every 10 presses #####################
###############################################################################################

# Open database connection
    db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

# prepare a cursor for storing the temperature reading
    cursorb = db.cursor()

    sql_update = """UPDATE fob_b set Fob_Batt_Pcnt = '"""+str(battpct)+"""'
                     where Fob_ID ='"""+Fob_ID+"""'"""
    try:
       cursorb.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('Scanner Job Error writing Battery percent', err)
       db.rollback()

	   
	   
print "***********************************************************************"
print "** Starting Protosen - the scanner process to read temps from sensor **"
print "***********************************************************************"
print
# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list

#sleep (30)
# find out from the params table what type of sensor is installed
SensorMode = get_Sensor_Mode()
DebugMode = get_debug()
print "Sensor mode parameter found: " + SensorMode

print "Opening connection and waiting for response...."
#write_log ('Scanner Job', 'Startup')
sleep (1)

# we need to send an email on start up, this is useful to alert the user the process has started up, 
# for instance after a power cut.  if the router is slow to start up the email send can fail, so we need
# to try a few times with a short delay.  if eventually it doesnt work, lets not lose any sleep, just
# write to the log and carry on.					  
global sendok
sendok = False
sendcounter = 0
while sendcounter < 10:
  sendcounter += 1
  
  send_alert('TC9000 Alert: Primary Sensor Scan process (v3.1.1) - STARTUP','Process start successful.')
  sendok = True




  if sendok:
    sendcounter = 11;  
    write_log('Scanner Job','Started up ok - email sent')
  else:
    print "Protosen Email error - sleeping for 15 seconds before retrying"
    sleep (15)
    
#  sending the email is not essential so if it failed after 10 goes, lets continue anyway
if not sendok:
  write_log('Scanner Job Main','Startup - sending email failed, but continuing anyway') 
  print "Protosen - Email failed, but running main program anyway"	
else:
  print "ProtoSen - Email sent ok - startup complete"


# read the time
  now = datetime.datetime.now()

# I realise this next IF is a bit naff, but it'll do for now and i'll sort it out properly in the future when i'm rich
if SensorMode == "SERIAL":
  ser = serial.Serial(DEVICE, BAUD)
#flush the serial port to clear out any unwanted data before starting
  ser.flushInput()

  msg = 'monitor initialised : ' + now.strftime("%H:%M %m-%d-%Y")
#
# Start infinite while loop to listen to XRF module
  while 1 :
   # All XRF module read and write commands should have 12 characters and begin with the letter "a"
   # Wait for message, the 1 second pause seems to improve the reading when several messages
   # are arriving in sequence, such as: a--TMP22.12-a--AWAKE----a--BATT2.74-a--SLEEPINGtime.
     time.sleep(0.1)
     while ser.inWaiting()>0:
#      This is inside loop so it can be turned on without a restart
       DebugMode = get_debug()
       buf = 'x'
       while buf[0] !='a':
         llapMsg = ser.read(12)
         if DebugMode == "Y":
           print "DEBUG: llapMSG = " + llapMsg
           print now
#  display packet, helps to troubleshoot any errors
         now = datetime.datetime.now()
         now.strftime("%H:%M %m-%d-%Y")
#       print 'Received '+ llapMsg + ' at ' + str(now)
     
         if "@" in llapMsg:
           if DebugMode == "Y":
             print "found a @ i llap, ignoring it"
#         read an single char to realign things		  
           llapMsg = ser.read(1)
         else: 
           
           now = datetime.datetime.now()
           now.strftime("%H:%M %m-%d-%Y")
     
# new sensors are format aZ1TEMP24.33
# old sensors are format aZ2TMP023.33
           if 'TMP' in llapMsg:	

             if DebugMode == "Y":
               print "DEBUG: found a TMP - new sensor in serial messages"		
               print ""
             llap_sensor_id = llapMsg[1:3]
             llap_temp = llapMsg[7:12]   

             if DebugMode == "Y":
#              print "DEBUG: llaptype found was " + llap_type 
               print "DEBUG: llap payload found was " +  llap_temp
               print "DEBUG: llap_sensor_id was " + llap_sensor_id
               print "DEBUG: llap temp was" + llap_temp

  # now write it to the db
             writeTemp(llap_sensor_id, llap_temp)
   
           if "TEMP" in llapMsg:
             if DebugMode == "Y": 
               print "DEBUG: Found a TEMP - new sensor in serial messages"		

             llap_sensor_id = llapMsg[1:3]
             llap_temp = llapMsg[8:12]   

             if DebugMode == "Y":
#              print "DEBUG: llaptype found was " + llap_type 
               print "DEBUG: llap payload found was " +  llap_temp
               print "DEBUG: llap_sensor_id was " + llap_sensor_id
               print "DEBUG: llap temp was" + llap_temp

  # now write it to the db
             writeTemp(llap_sensor_id, llap_temp)

           if 'FOB' in llapMsg:

             if DebugMode == "Y":
               print "DEBUG: Detected a button press"
               print ""
               llap_fob_id = llapMsg[1:3]
               print "DEBUG: llap_fob_id = " + llap_fob_id 
               llap_fob_name = llapMsg[3:9]
               print "DEBUG: llap_fob_name = " + llap_fob_name
               llap_fob_butt = llapMsg [9:10]
               print "DEBUG: llap_fob_butt" + llap_fob_butt




           if 'BATT' in llapMsg :

        # Battery reading sent
             if DebugMode == "Y":
               print "DEBUG: Battery level is " + llapMsg[7:11] + "V"
           # Save this value for later.
             batt = llapMsg[7:11]
             sensor_id =llapMsg[1:3]

             if llapMsg[1:2] == "Z":
               zone_id, found_zone_ind = get_zone(sensor_id)
           
               if found_zone_ind:
                 if DebugMode == "Y":
                   print "DEBUG: " + str(zone_id)
                   print "DEBUG: zone found "

                 battlevel = float(batt)
                 battpcnt = int(float(battlevel / 3)*100)
# new batteries can read slightly over, so max out the reading at 100% 

                 if battpcnt > 100:
                   battpcnt = 100
                 writeBatt(str(zone_id), battpcnt)
               else:
                 continue
else:
#run code for UDP Sensors
# Set up the UDP socket
  sock = socket.socket(socket.AF_INET, # Internet
              socket.SOCK_DGRAM) # UDP

  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    
  sock.bind(('', FROM_PORT))
  print "Entering UDP loop"
  while 1 :
   # All XRF module read and write commands should have 12 characters and begin with the letter "a"
   # Wait for message, the 1 second pause seems to improve the reading when several messages
   # are arriving in sequence, such as: a--TMP22.12-a--AWAKE----a--BATT2.74-a--SLEEPINGtime.
#   time.sleep(0.1)

    if DebugMode == "Y":
      print ""
      print "DEBUG: Waiting on socket for data to arrive......"		
    data, addr = sock.recvfrom(1024)
    if DebugMode == "Y":
      print("DEBUG: Got: {} from address {}".format(data, addr))   


    llap_type = data[102:106]
    if DebugMode == "Y":
      print "DEBUG: llap_type = " + llap_type
    now = datetime.datetime.now()
    now.strftime("%H:%M %m-%d-%Y")
     
 
    if 'TEMP' in llap_type:	
# message from a new white sensor	
      llap_sensor_id = data[122:124]
      llap_temp = data[106:111]   

      if DebugMode == "Y":
        print "DEBUG: llaptype found was " + llap_type 
        print "DEBUG: llap payload found was " + data[102:111]
        print "DEBUG: llap_sensor_id was " + llap_sensor_id

  # now write it to the db
      writeTemp(llap_sensor_id, llap_temp)

   
    if 'BATT' in llap_type :

#   Battery reading sent
      batt = data[106:110]
      llap_sensor_id = data[121:123]
      llap_batt_sensor_type = data[121:122]
#      print sensor_id

# we need to work out if its a battery reading for a fob or a temp sensor, only way to do this is with the ID
# temp sensor start with a Z, fobs start with an FOB
 

      if DebugMode == "Y":
        print "DEBUG: Battery reading for sensor type (F/Z) of " + llap_batt_sensor_type
      if llap_batt_sensor_type == "Z":
        zone_id, found_zone_ind = get_zone(llap_sensor_id)
        if DebugMode == "Y":
          print "DEBUG: ***  BATT ***  Sensor " + llap_sensor_id + " gave battery level of " + batt     
        if found_zone_ind:
          battlevel = float(batt)
          battpcnt = int(float(battlevel / 3)*100)
          if battpcnt > 100:
            battpcnt  = 100        
          writeBatt(str(zone_id), battpcnt)
        else:
          print "ERROR: Didn't find the zone for that battery reading, no drama"
     
      if llap_batt_sensor_type == "F":
        battlevel = float(batt)
        battpcnt = int(float(battlevel / 3)*100)
        if battpcnt > 100:
          battpcnt  = 100
        update_fob_batt(llap_sensor_id, battpcnt)
        if DebugMode == "Y":
          print "DEBUG: ***  BATT ***  Sensor " + llap_sensor_id + " gave battery level of " + batt     
 
	 
	 
	 
# old sensor in via message bridge and UDP port
    if 'TMP' in llap_type:	
      if DebugMode == "Y":
        print "DEBUG: Found a TMP - old sensor in UDP messages"
      llap_sensor_id = data[122:124]
      llap_temp = data[106:111]
      if DebugMode == "Y":	  
        print "DEBUG: Got temp of " + llap_temp
      if DebugMode == "Y":
        print "DEBUG: llaptype found was " + llap_type 
        print "DEBUG: llap payload found was " + data[102:111]
        print "DEBUG: llap_sensor_id was " + llap_sensor_id

  # now write it to the db
      writeTemp(llap_sensor_id, llap_temp)
  
    if 'FOB' in llap_type:
      llap_fob_name = data[102:108]
      llap_fob_id = data[120:122]
      llap_fob_butt = data[108:109]
      if DebugMode == "Y":
        print "DEBUG: Detected a fob button press"
        print "DEBUG: llap_fob_id = " + llap_fob_id 
        print "DEBUG: llap_fob_name = " + llap_fob_name
        print "DEBUG: llap_fob_butt = " + llap_fob_butt
      get_fob_action(llap_fob_id, llap_fob_butt)

      
# End of UDP code
  
print "ERROR: We should never get here.......somethings gone wrong"
send_alert ('Scanner Job', 'We have exited the main protosen loop, something has gone wrong, call ghost busters')
write_log ('Scanner Job', 'Main loop exit unexpected')
