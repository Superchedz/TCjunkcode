################################################################################################
#                                       Logger.py
#                                       =========
################################################################################################
#  This program is part of the TotalControl9000 system.
#  This program is called to simply write to the log.  This allows shell scripts to write to the
#  log_b table.  The data written to the table is passed into this program via run command params.
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2015-11-22 GLC   Added to receive params from run command.
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
######################################      Main     ###########################################
################################################################################################


print "***********************************************************************"
print "** Starting Logger - just a program to write to the log table        **"
print "***********************************************************************"
print
# have a short delay to allow the DB to be started up on reboot
# really this should be replaced with a retry on the open - put it on the todo list
# sleep (30)
# not really needed for the logger process.


firstparam = str(sys.argv[1])
secondparam = str(sys.argv[2])



write_log (firstparam, secondparam)

