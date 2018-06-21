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
  global Shutdown
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
    else:
      Shutdown = Shutdown_res[1]
      return Shutdown
  else:
    critical_error('Get Shutdown', 'ERROR : Missing Shutdown Param', '--!! Shutting down ^2 !!--')
    print "***  Error:  Missing Param Shutdown param  ***"

	
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
 


write_log('Main','Closing down - shouldnt be doing this really')
db.close()
