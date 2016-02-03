################################################################################################
#                                       Protosen.py 
#                                       ==========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program monitors the serial port and reads in the temperature sensor readings.  It
#  matches the sensor ID with a zone_id in the database and writes the record to the 
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
#  1.3      2016-02-03 GLC   Removed sleep at start as have moved it to cron to support git
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

#
# SETTINGS
#
# Default settings for program; port, baud rate, temperature threshold, number of readings to store
# set up serial port for temperature readings
DEVICE = '/dev/ttyAMA0'
BAUD = 9600
# END OF SETTINGS

################################################################################################
###################### Function to write to the event log table ################################
################################################################################################

def write_log(Log_From, Log_Text):
  print "************** Creating log***************"

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
    critical_error('Get ServerSMTP', 'ERROR : Missing', '--!! Shutting down ^2 !!--')
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
    print "***  Error:  Missing Param EmailPwd  ***"
    critical_error('Get Email Password', 'ERROR : Missing', '--!! Shutting down ^2 !!--')
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

def writeTemp(zone_id, temp):

    now = datetime.datetime.now()
# Open database connection
    db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

# prepare a cursor for storing the temperature reading
    cursor = db.cursor()
    zone_id_short = zone_id[1:2]
    
# Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO zone_temp_hist_b (log_date,
                                           zone_id,
                                           temperature)
             VALUES ('"""+str(now)+"""','"""+zone_id_short+"""',"""+str(temp)+""")"""
   
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
#
#    # prepare a cursor for storing just the current temperature reading against the zone record
    cursor3 = db.cursor()
#
#    # Prepare SQL query to UPDATE a record into the database.
    sql_update = """UPDATE zone_b set Zone_Last_Temp_Reading = '"""+str(temp)+"""',
                              Zone_Last_Temp_Reading_Dtime = '"""+str(now)+"""'
                     where Zone_ID ='"""+zone_id_short+"""'"""
    try:
       cursor3.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('ProtoSen Error writing temps', err)
       db.rollback()
    db.close()


def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False

	  
def get_zone(sensor_id):

# Open database connection
  db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

  zone_cursor = db.cursor ()
  zone_query = ("""select Zone_ID from zone_b where Zone_Sensor_ID = '%s'""" % (sensor_id))

  try:
     zone_cursor.execute(zone_query)
  except MySQLdb.Error as err:
     print ("******* Error reading get_zone : ERROR : {}".format(err))
     write_log ('Get Zone',err)
     critical_error('Get Zone', 'ERROR : Cursor in getzone', '--!! Shutting down ^2 !!--')

  numrows = int (zone_cursor.rowcount)

  if numrows == 1:
    zone_id = zone_cursor.fetchone()
    zone_found_ind = True
  else:
    zone_id = 0
    zone_found_ind = False
    if numrows > 1:
#      print "***  Error:  Multiple Zones with same sensor id Error  ***"
      send_alert('Alert: Protosen - *** Error ***','Multiple Zones with same sensor ID - Shutting down %s' % str(sensor_id))
      write_log ('ProtoSen ERROR multiple zones configured for a single sensor', str(sensor_id))
      critical_error('Get Zone', 'ERROR : Multiple Zones set for a Sensor', '--!! Shutting down ^2 !!--')
    if numrows == 0:
#      print "***  Warning:  No Zone set for sensor id - Warning ***"
      send_alert('Warning: Protosen - *** Warning ***','Sensor reading recieved for unconfigured sensor - check config')
      write_log ('ProtoSen: Warning no zone configured for sensor', str(sensor_id))
  return (zone_id, 	zone_found_ind) 


  
def writeBatt(zone_id, battpct):

#    now = datetime.datetime.now()
# Open database connection
    db = MySQLdb.connect("localhost","root","pass123",db = "BoilerControl" )

# prepare a cursor for storing the temperature reading
    cursor = db.cursor()
    zone_id_short = zone_id[1:2]
    
#
#    # prepare a cursor for storing just the current temperature reading against the zone record
    cursorb = db.cursor()
#
#    # Prepare SQL query to UPDATE a record into the database.
    sql_update = """UPDATE zone_b set Zone_Sensor_Batt_Pcnt = '"""+str(battpct)+"""'
                     where Zone_ID ='"""+zone_id_short+"""'"""
    try:
       cursorb.execute(sql_update)
       db.commit()
    except MYSQLdb.Error as err:
       write_log ('ProtoSen Error writing Battpcnt', err)
       db.rollback()
#

print "***********************************************************************"
print "** Starting Protosen - the scanner process to read temps from sensor **"
print "***********************************************************************"
print
# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list

sleep (30)

print "Opening connection and waiting for response..."
#
ser = serial.Serial(DEVICE, BAUD)
write_log ('ProtoSen', 'Startup')


# we need to send an email on start up, this is useful to alert the user the process has started up, 
# for instance after a power cut.  if the router is slow to start up the email send can fail, so we need
# to try a few times with a short delay.  if eventually it doesnt work, lets not lose any sleep, just
# write to the log and carry on.					  
global sendok
sendok = False
sendcounter = 0
while sendcounter < 10:
  sendcounter += 1				  
  send_alert('TC9000 Alert: Sensor Scanner Job - STARTUP','System starting')
  if sendok:
    sendcounter = 11;  
    write_log('Scanner Main','Starting up ok - email sent')
  else:
    print "Protosen Email error - sleeping for 15 seconds before retrying"
    sleep (15)
    
#  sending the email is not essential so if it failed after 10 goes, lets continue anyway
if not sendok:
  write_log('Protosen Main','Startup - sending email failed, but continuing anyway') 
  print "Protosen - Email failed, but running main program anyway"	
else:
  print "ProtoSen - Email sent ok - startup complete"


# read the time
now = datetime.datetime.now()
#flush the serial port to clear out any unwanted data before starting
ser.flushInput()
print now
msg = 'monitor initialised : ' + now.strftime("%H:%M %m-%d-%Y")
#
# Start infinite while loop to listen to XRF module
while 1 :
   # All XRF module read and write commands should have 12 characters and begin with the letter "a"
   # Wait for message, the 1 second pause seems to improve the reading when several messages
   # are arriving in sequence, such as: a--TMP22.12-a--AWAKE----a--BATT2.74-a--SLEEPINGtime.
   time.sleep(0.1)

   while ser.inWaiting()>0:
     buf = 'x'
     while buf[0] !='a':
       llapMsg = ser.read(12)
       print llapMsg
#  display packet, helps to troubleshoot any errors
       now = datetime.datetime.now()
       now.strftime("%H:%M %m-%d-%Y")
#       print 'Received '+ llapMsg + ' at ' + str(now)
     
       if "@" in llapMsg:
          print "found a @ i llap, ignoring it"
#         read an single char to realign things		  
          llapMsg = ser.read(1)
       else: 
         if 'TMP' in llapMsg:
 
           temp = llapMsg[7:12]
# we need to make sure the temp is always just 2dp to match the database field        
           if is_number(temp) == True:
             sensor_id =llapMsg[1:3]
             zone_id, found_zone_ind = get_zone(sensor_id)
             if found_zone_ind:             
               temp2dp = float(float(int(float(temp)*100)) / 100)
# now write it to the db
               writeTemp(str(zone_id), temp2dp)
# we don't need an else here as unfound zones are handled in the called function
           else:
#             print "Temp reading was not numeric so ignoring"
#             print 'Received '+ llapMsg + ' at ' + str(now)
# take a character off the port to try and resync.
#             print "Reading extra 1 char"
             llapMsg = ser.read(1)
          

         if 'BATT' in llapMsg :

           # Battery reading sent
#           print "Battery level is " + llapMsg[7:11] + "V"
           # Save this value for later.
           batt = llapMsg[7:11]
           sensor_id =llapMsg[1:3]

           zone_id, found_zone_ind = get_zone(sensor_id)
           
           if found_zone_ind:
#             print str(zone_id)
#             print "zone found "

             battlevel = float(batt)
             battpcnt = int(float(battlevel / 3)*100)
        
             writeBatt(str(zone_id), battpcnt)
           else:
             continue
#             print "no zone found for batt so doing nothing with reading"
         #
         # Is it an temp reading?
#         if 'TMP' in llapMsg :
         # reading sent
         #
#            print "Zone id = " + zone_id + " has temp of " + temp + " degrees Celcius"
           
            # temp is a 1 element array, hence the "[" "]"
            #except ValueError:
            # if float operation fails, skip bad reading
            #   print "bad reading"
         #
#   ser.flushInput()
#
# for want of a better phrase,- endwhile
# end of program
print "We should never get here.......somethings gone wrong"
send_alert ('ProtoSen', 'We have exited the main loop, something has gone wrong, call ghost busters')
write_log ('ProtoSen', 'Main loop exit unexpected')
