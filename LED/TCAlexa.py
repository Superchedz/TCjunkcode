################################################################################################
#                                       TCAlexa.py
#                                       ==========
################################################################################################
#  
#  This program is part of the TC9000 system.  TCAlexa.py is the back end service for the Alexa
#  voice control function.  This program is run on start up and runs constantly.  When Alexa
#  is called to perform an action, Alexa, via an NGROK https tunnel call this program.  This
#  program can perform the following functions:
#
#  Boost       - boosts a zone
#  Status      - return the current status of a zone
#  Cancel      - cancels an existing boost for an active zone
#  Preset      - runs a predefined boost for a zone as set at zone level
#  
################################################################################################
#  Change History
#  ==============
#  Version  Date       Who   Description
#  ======== ========== ====  ===========
#  1.0      2014-11-01 GLC   Initial Version
#  1.1      2019-01-01 GLC   Bit of a tidy up and continue dev
#  1.2      2019-01-11 GLC   Finalised code for first deployment
#  1.3      2019-01-28 GLC   Improved help and added fallback intent

from flask import Flask
from flask_ask import Ask, statement, question, session

import json
import requests
import time
import sys 
import MySQLdb 
import datetime
from getpw import getpass

#import unidecode


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
################# Function to write to the alexa_temp_boost_b table ############################
################################################################################################

def write_alexa_temp_boost(AlexaZoneID, Alexadurationmins, Alexaboosttemp):


# before we insert, we should always delete as old data is always superceeded

  global Error_state
  Error_state = False
  alexa_clean = db.cursor()

  try:
    alexa_clean.execute("DELETE FROM alexa_temp_boost_b")
  except MySQLdb.Error as err:
    print "oh no!!! There was an error deleting from the alexa table"
    write_log ('Alexa Cleaner', '*** ERROR *** Deleting from alexa')
#    send_alert('Alexa Cleaner Error', '***Error detected deleting from alexa boost table')
    Error_state = True
    db.rollback()
  alexa_clean.close() 

  if Error_state == False:
    alexa_cursor = db.cursor()
 
    sql = """INSERT INTO alexa_temp_boost_b (Alexa_Zone_ID, Alexa_duration_mins, Alexa_boost_temp) VALUES ('"""+str(AlexaZoneID)+"""','"""+str(Alexadurationmins)+"""','"""+str(Alexaboosttemp)+"""')""" 
    
    try:
       alexa_cursor.execute(sql)
       db.commit()

    except MySQLdb.Error as err:
       db.rollback()
       write_log ('Alexa Insert', '*** ERROR *** inserting Alexa boost')       
       print ("***** Error on alexa insert: ERROR: {}".format(err))
       Error_state = True       

    alexa_cursor.close() 	
    db.commit()

################################################################################################
############################### Function to get debug mode flag ################################
################################################################################################


def get_alexa_param():

  alexa_cursor = db.cursor ()
  alexa_query = "select * from params_b where Param_Name = 'Alexa_YN'"
  global AlexaYN
  try:
     alexa_cursor.execute(alexa_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Alexa_YN param : ERROR : {}".format(err))
     write_log ('ERROR: Get Alexa_YN',err)

  numrows = int (alexa_cursor.rowcount)
  if numrows == 1:
    alexa_res = alexa_cursor.fetchone()
    if alexa_res[1] != "Y" and alexa_res[1] != "N":
      print ""
      print "*******  ERROR : Alexa YN param is not numeric  *********"
    else:
      AlexaYN = alexa_res[1]
      return AlexaYN
  else:
    print "***  Error:  Missing Param Alexa_YN param  ***"

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
      print "*******  ERROR : Loop_DebugMode param is not numeric  *********"
    else:
      DebugMode = Debug_res[1]
      return DebugMode
  else:
    print "***  Error:  Missing Param Debugmode param  ***"


################################################################################################
############################### Function to get preset details   ###############################
################################################################################################

def get_preset_zone(keyword):

  global zonefound
  zonefound = False
  
  presetzone_cursor = db.cursor ()
  presetzone_query = ("""select Zone_ID, Zone_Name, Zone_Active_Ind, Zone_Current_State_Ind, alexa_temp, alexa_duration, Zone_Type, Zone_Last_Temp_Reading  from zone_b where REPLACE (alexa_keyword, ' ','') = REPLACE('%s', ' ', '')""" % (keyword))
                             
  try:
     presetzone_cursor.execute(presetzone_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Alexa presets : ERROR : {}".format(err))
     write_log ('ERROR: Get Alexa preset',err)

  numrows = int (presetzone_cursor.rowcount)

  if numrows == 1:
    preset_res = presetzone_cursor.fetchone()
    zonefound = True
    presetzone_cursor.close() 	
    db.commit()
    return preset_res
  else:
    presetzone_cursor.close() 	
    db.commit()
    return 


###########################################  functions to convert alexa duration to mins and validate it ###################################################
def conv_duration(alexa_duration):
  global durationok
  durationok = True
  try:
    totalmins = alexa_duration.total_seconds()/60
  except:
    print "Error converting the duration"
    write_log ('Alexa bad duration', str(alexa_duration))
#    return statement('the duration you provided could not be determined, i think you said something about potatoes - check the log for details')
    durationok = False
    totalmins = 0       
  return int(totalmins)
  

########################################### get the zone details from the zone number #########################################################

def get_zone(zone_id):

  global zonename
  global zonefound
  zonefound = False
  zonename_cursor = db.cursor ()
  
  zonename_query = """select Zone_Name,Zone_Active_Ind, Zone_Current_State_Ind, Zone_Last_Temp_Reading, Zone_Type from zone_b where Zone_ID = %d""" % (zone_id)
   
  try:
     zonename_cursor.execute(zonename_query)
  except MySQLdb.Error as err:
     print ("******* Error reading Zone_Name : ERROR : {}".format(err))
     write_log ('ERROR: Get Zone_Name for alexa boost',err)

  numrows = int (zonename_cursor.rowcount)
  if numrows == 1:
    zoneres = zonename_cursor.fetchone()
    zonefound = True
    zonename_cursor.close() 	
    db.commit()
    return zoneres
  else:
    zonefound = False
    return "Zone not found error"
  
  zonename_cursor.close() 	
  db.commit()



###################################################### start of code #################################


dbpass = getpass()

db = MySQLdb.connect (host   = "localhost",
                      user   = "TCROOT9000",
                      passwd = dbpass,
                      db     = "BoilerControl")

DebugMode = get_debug()
zonefound = False

app = Flask(__name__)
ask = Ask(app, "/")
################################################################################################

print "" 
print "#########################################" 
print "########## Welcome to TCAlexa ###########"
print "##########    Version 1.0    ############"
print "#########################################" 
print ""



def get_headlines():
    pass

@app.route('/')

@ask.launch
def welcome():
   Alexa_YN =get_alexa_param()
   if Alexa_YN == "Y":
     return question("Welcome to TOTAL CONTROL 9000, say the boost or preset command, cancel active boosts, or request the status of a zone, or say total control for help.")
   else:
     return statement("Your Total Control 9000 system is not configured to use the Alexa Service, please check your configuration")


############################################################################################################################################
################################################################     NO   ##################################################################
############################################################################################################################################
  

@ask.intent("NoIntent")
def gono():

   nonomsg = "ok, the boost was not applied, good bye"
   return statement(nonomsg)




############################################################################################################################################
##################################################   Setup the boost request with temp #####################################################
############################################################################################################################################
  
@ask.intent("BoostIntent", convert={'zone':str, 'duration': 'timedelta', 'temperature':int})

# this code is for zones that are type T with a temperature sensor, but you can use it for any zone but the temperature is not really
# needed.  for Not temp zones, best to set up a special intent in the boostNTIntent so you can say "water the greenhouse for 20 mins"

def boost(zone, duration, temperature):
   global zonefound
   global Error_state
   global durationok
#####   zoneID = int(zone)
   
# its possible the db connection has timeout, so ping first to reopen the connection
   db.ping(True)

   mins_duration = conv_duration(duration)
   if durationok == False:
     return statement('the duration you provided could not be determined, i think you said something about potatoes - check the log for details')

   if ' ' in zone:
     boost_msg = 'A space was detected in your zone name of ' + str(zone) + '.  Please check your zone configuration and adjust your pronunciation'
     write_log ('Alexa bad boost request - contained spaces', zone)
     return statement(boost_msg)
   else:
     if str.isdigit(zone) == True:

       zoneID = int(zone)
       ZoneRES = get_zone(zoneID)
 
       if zonefound == True:
         zonename = ZoneRES[0]
         zoneactiveind = ZoneRES[1]
         zonecurrentstate = ZoneRES[2]
         zonetype = ZoneRES[4]
  
         if DebugMode == "Y":
           print "The zone requested was " + str(zone)
           print "with a duration of " + str(mins_duration)
           print "The temperature is " + str(temperature)
           print ZoneRES
     else:
       zoneRES = get_preset_zone(zone)
       if zonefound == True:
         zoneID = zoneRES[0]
         zonename = zoneRES[1]
         zoneactiveind = zoneRES[2]
         zonecurrentstate = zoneRES[3]
         zonetype = zoneRES[6]

     if zonefound == True:
       if zoneactiveind == "Y":
         if zonecurrentstate == "OFF":
           boost_msg = 'The zone requested was ' + str(zonename) + ', with a duration of ' + str(mins_duration) + ' minutes, at ' + str(temperature) + ' degrees, is that correct?'
         else:
           boost_msg = 'The zone requested was ' + str(zonename) + ', with a duration of ' + str(mins_duration) + ' minutes, at ' + str(temperature) + ' degrees, this zone is already running, is it ok to replace that boost with this one?'
         write_log ('Alexa boost, ok', zonename)
         write_alexa_temp_boost(zoneID, mins_duration, temperature)
         return question(boost_msg)
       else:
         boost_msg = 'You requested a boost on the ' + str(zonename) + 'zone, unfortunately this zone is currently deactivated, please reactivate via the website before attempting any boost'
         write_log ('Alexa bad boost, zone deactivated', zonename) 
         return statement(boost_msg)
     else:
       boost_msg = 'The zone requested of ' + str(zone) + 'was not found, please try again'
       write_log ('Alexa bad boost, zone not found', zone) 
       return statement(boost_msg)



############################################################################################################################################
#################################################   Setup the boost request with NO temp ###################################################
############################################################################################################################################
  
@ask.intent("BoostNTIntent", convert={'zone':str, 'duration': 'timedelta'})

def boostNT(zone, duration):

# this code is for zones that are NOT type T with no temperature sensor
# we just default the temperature to 1

   global zonefound
   global Error_state
   global durationok
   temperature = 1
#####   zoneID = int(zone)
   
# its possible the db connection has timeout, so ping first to reopen the connection
   db.ping(True)
   
   mins_duration = conv_duration(duration)
   if durationok == False:
     return statement('the duration you provided could not be determined, i think you said something about potatoes - check the log for details')
  
   
   if ' ' in zone:
     boost_msg = 'A space was detected in your zone name of ' + str(zone) + '.  Please check your zone configuration and adjust your pronunciation'
     write_log ('Alexa bad boost NT request - contained spaces', zone)
     return statement(boost_msg)
   else:
     if str.isdigit(zone) == True:
       print "its a number so lets assume its the zone number"
       zoneID = int(zone)
       ZoneRES = get_zone(zoneID)
 
       if zonefound == True:
         zonename = ZoneRES[0]
         zoneactiveind = ZoneRES[1]
         zonecurrentstate = ZoneRES[2]
         zonetype = ZoneRES[4]
         if DebugMode == "Y":
           print "The zone requested was " + str(zone)
           print "with a duration of " + str(mins_duration)
           print "The temperature is hardcoded" + str(temperature)
           print ZoneRES
     else:
       zoneRES = get_preset_zone(zone)
       if zonefound == True:
         zoneID = zoneRES[0]
         zonename = zoneRES[1]
         zoneactiveind = zoneRES[2]
         zonecurrentstate = zoneRES[3]
         zonetype = zoneRES[6]
         
     if zonefound == True:
       if zonetype == "T":
         boost_msg = 'The zone requested of ' + str(zone) + 'has a temperature sensor and so this request was invalid, please use the preset or boost commands'
         write_log ('Alexa bad boost, BoostNT request for T zone', zone) 
         return statement(boost_msg)
       if zoneactiveind == "Y":
         if zonecurrentstate == "OFF":
           boost_msg = 'The zone requested was ' + str(zonename) + ', with a duration of ' + str(mins_duration) + 'minutes is that correct?'
         else:
           boost_msg = 'The zone requested was ' + str(zonename) + ', with a duration of ' + str(mins_duration) + 'minutes, this zone is already running, is it ok to replace the current boost with this one?'
         write_log ('Alexa boost, ok', zonename)
         write_alexa_temp_boost(zoneID, mins_duration, temperature)
         return question(boost_msg)
       else:
         boost_msg = 'You requested a boost on the ' + str(zonename) + 'zone, unfortunately this zone is currently deactivated, please reactivate via the website before attempting any boost'
         write_log ('Alexa bad boost, zone deactivated', zonename) 
         return statement(boost_msg)
     else:
       boost_msg = 'The zone requested of ' + str(zone) + 'was not found, please try again'
       write_log ('Alexa bad boost, zone not found', zone) 
       return statement(boost_msg)

############################################################################################################################################
################################################################   Preset   ################################################################
############################################################################################################################################
@ask.intent("PresetIntent",convert={'keyword': str})
def preset(keyword):  
   global zonefound   
   Error_state = False
   zonefound = False
   
# its possible the db connection has timeout, so ping first to reopen the connection
   db.ping(True)

# get the params for the preset keyword
   if ' ' in keyword:
     preset_msg = 'A space was detected in your zone name of ' + str(keyword) + '.  Please check your zone configuration and adjust your pronunciation'
     return statement(preset_msg)
   else:

     presetRES = get_preset_zone(keyword)

     if zonefound == True:
       
       zone = presetRES[0]
       zonename = presetRES[1]
       zoneactiveind = presetRES[2]
       zonecurrentstate = presetRES[3]
       temperature = presetRES[4]
       duration = presetRES[5]
       zonetype = presetRES[6]
            
       if zoneactiveind == "Y":
         if zonecurrentstate == "OFF":
           if zonetype == "T":
             preset_msg = 'Your preset is to boost the ' + str(zonename) + 'zone, for ' + str(duration) + 'minutes at ' + str(temperature) + 'degrees , is that correct?'
           else:
             preset_msg = 'Your preset is to boost the ' + str(zonename) + 'zone, for ' + str(duration) + 'minutes, is that correct?'
         else:
           if zonetype == "T":
             preset_msg = 'Your preset is to boost the ' + str(zonename) + 'zone, for ' + str(duration) + 'minutes at' + str(temperature) +  'degrees, this zone is already running, is that ok?'
           else:
             preset_msg = 'Your preset is to boost the ' + str(zonename) + 'zone, for ' + str(duration) + 'minutes, this zone is already running, is that ok?'
         write_alexa_temp_boost(zone, duration, temperature)
         write_log ('Alexa preset, temp record saved ok', keyword) 
       else:
         preset_msg = 'The ' + str(zonename) + ' zone linked to this preset is currently deactivated, please reactivate via the website before boosting'
         write_log ('Alexa bad preset, zone deactivated', keyword) 
         return statement(preset_msg)
     else:
       #preset_msg = 'The ' + str(keyword) + ' preset you requested was not found, please check your spelling, speak more clearly, dont mumble and also avoid weird accents.....such as saying your in the par shar for half an are'
       preset_msg = 'The ' + str(keyword) + ' preset you requested was not found, Please check your zone configuration and adjust your pronunciation'
       write_log ('Alexa bad preset request - keyword not found', keyword) 
       return statement(preset_msg)
   return question(preset_msg)


############################################################################################################################################
##########################################################   Confirm a boost  ##############################################################
############################################################################################################################################
    
@ask.intent("YesIntent")

def yes():
   global zonefound

###############################  this means everything is set up, so just move from the alexa_temp_boost table to the override table ###########


# first get the temporary boost record we stored earlier

   alexa_temp_boost_cursor = db.cursor()

   try:
       alexa_temp_boost_cursor.execute("SELECT * from alexa_temp_boost_b")
   except MySQLdb.Error as err:
       print ("******* Error reading Alexa Boost : ERROR : {}".format(err))
       write_log ('ERROR: Selecting the stored alexa request',err)
       confirmmsg = "Something went wrong processing the boost record, your house will now explode...5...4...3...2...1.....parp"
       return statement(confirmmsg)

   numrows = int(alexa_temp_boost_cursor.rowcount)
   if numrows == 0:
      write_log ('ERROR: Row not found alexa code #1',err)
      confirmmsg = "Somethings gone wrong, there doesn't seem to be a boost to confirm right now, please try again from the start"
      return statement(confirmmsg)
   if numrows > 1:
      write_log ('ERROR: Unexpected data in alexa code #2',err)
      confirmmsg = "Somethings gone wrong, there seems to be more than one boost pending confirmation, you'd better call Graham"
      return statement(confirmmsg)     
   if numrows == 1:
      atb_res = alexa_temp_boost_cursor.fetchone()
      if DebugMode == "Y":
        print "Alexa temp row found:zone %d temp: %d Duration : %d" % (atb_res[0], atb_res[1], atb_res[2])
      boost_zone = atb_res[0]
      boost_duration = atb_res[1]
      boost_temp = atb_res[2]

# now insert the proper override record into the database 
      now = datetime.datetime.now()
      boost_end = now + datetime.timedelta(minutes =boost_duration)
      if DebugMode == "Y":
        print boost_end
# before we do, its wise to delete any active boosts for the zone as we could end up with 2 at a time
      override_clean = db.cursor()
      try:
          override_clean.execute("DELETE FROM override_b where Zone_id = %s and Override_end > NOW()", (boost_zone))
#     dont worry about the number of rows found, doesn't matter    
      except MySQLdb.Error as err:
         print "oh no!!! There was an error deleting from the override table"
         write_log ('Alexa Cleaner', '*** ERROR *** Deleting from override')
         db.rollback()
         confirmmsg = "Something went wrong processing the boost record, your house will now explode...5...4...3...2...1.....parp"
         return statement(confirmmsg)

      override_clean.close() 
  
# Prepare SQL query to INSERT a record into the database.
      cursor = db.cursor()
#      zone_id_short = boost_zone[1:2]
      confirmmsg = "That's great, your boost is confirmed and active, you can use the cancel command at anytime.  Goodbye"
      write_log ('Alexa boost request', 'Confirmed and applied') 

      sql = """INSERT INTO override_b (zone_id,
                                       Override_start,
                                       Override_end,
                                       Override_Duration_mins,
                                       Override_Temp)
               VALUES ('"""+str(boost_zone)+"""','"""+str(now)+"""','"""+str(boost_end)+"""','"""+str(boost_duration)+"""','"""+str(boost_temp)+"""')"""
      try:
          cursor.execute(sql)
          db.commit()
      except:
          print ("******* Error interting Alexa Boost : ERROR : {}".format(err))
          write_log ('ERROR: Interting alexa request into override',err)
          confirmmsg = "Something went wrong inserting the boost record, your house will now explode...5...4...3...2...1.....parp"
          db.rollback()
          return statement(confirmmsg)
      
   db.commit()
   return statement(confirmmsg)
   
############################################################################################################################################
#####################################################   Cancel an active boost on a zone ###################################################
############################################################################################################################################
  
@ask.intent("CancelIntent", convert={'cancelzone':str})
def cancel(cancelzone):
   global zonefound

   Error_state = False
   zonefound = False

# its possible the db connection has timeout, so ping first to reopen the connection
   db.ping(True)

# the request could be a zone id or the alexa keyword, so we need to handle either
   if ' ' in cancelzone:
     cancel_msg = 'A space was detected in your zone name of ' + str(cancelzone) + '.  Please check your zone configuration and adjust your pronunciation'
     write_log ('Alexa bad cancel request - contained spaces', cancelzone) 
   else:
     if str.isdigit(cancelzone) == True:
       zoneID = int(cancelzone)
       ZoneRES = get_zone(zoneID)
       if zonefound == True:
         zonename = ZoneRES[0]
     else:
       if cancelzone == "all":
         zonefound = True
       else: 
         cancelRES = get_preset_zone(cancelzone)
         if zonefound == True:
           zoneID = cancelRES[0]
           zonename = cancelRES[1]  
    
     if zonefound == True:
       write_log ('Alexa cancel request ok', cancelzone)      
       Override_clean = db.cursor()
       if cancelzone == "all":
         try:
             Override_clean.execute("DELETE FROM override_b WHERE Override_end > NOW()")
         except MySQLdb.Error as err:
             print "oh no!!! There was an error deleting from the override table in cancel"
             write_log ('Alexa SQL#44', '*** ERROR *** Deleting all from Override')
#        send_alert('Override Cleaner Error', '***Error detected deleting from Override during scheduled job')
             Error_state = True
       else:
         try:
             Override_clean.execute("DELETE FROM override_b WHERE Override_end > NOW() and Zone_ID = %s", (zoneID))
           
         except MySQLdb.Error as err:
             print "oh no!!! There was an error deleting from the override table in cancel"
             write_log ('Alexa SQL#42', '*** ERROR *** Deleting from Override for zone')
#        send_alert('Override Cleaner Error', '***Error detected deleting from Override during scheduled job')
             Error_state = True

       if not Error_state:  
         numrows = int (Override_clean.rowcount)
         if numrows == 0:
           
           if cancelzone == "all":
             cancel_msg =  'There were no active boosts found to cancel'
           else:
             cancel_msg =  'There were no active boosts found' +str(zonename) + 'zone to cancel'
         else:
           if cancelzone == "all":
             cancel_msg =  str(numrows) + ' active boosts were cancelled successfully, goodbye'
           else:
             cancel_msg =  'All active boosts on the ' +str(zonename) + ' zone were cancelled successfully, goodbye you edjit'
     else:
       if str.isdigit(cancelzone) == True:
         cancel_msg =  'The zone number ' +str(cancelzone) + ' could not be found, please try again, you dumbo.'
         write_log ('Alexa bad cancel request - zone num not found', cancelzone) 
       else:
         cancel_msg =  'No zone with a preset name of ' +str(cancelzone) + ' could be found, please try again.'
         write_log ('Alexa bad cancel request - zone keyword not found', cancelzone) 
     db.commit()
   return statement(cancel_msg)

############################################################################################################################################
##########################################################   Get Status for a Zone #########################################################
############################################################################################################################################
@ask.intent("StatusIntent", convert={'statuszone':str})
def Statuszone(statuszone):
   global zonefound
   Error_state = False

# its possible the db connection has timeout, so ping first to reopen the connection
   db.ping(True)
   
# the request could be a zone id or the alexa keyword, so we need to handle either
   
   if ' ' in statuszone:
     status_msg = 'A space was detected in your zone name of ' + str(statuszone) + '.  Please check your zone configuration and adjust your pronunciation'
     write_log ('Alexa bad status request - contained spaces', statuszone)    
   else:  
     if str.isdigit(statuszone) == True:
       
       zoneID = int(statuszone)
       ZoneRes = get_zone(zoneID)
       
       if zonefound == True:
         zonename = ZoneRes[0]
         zonetype = ZoneRes[4]
         zoneactiveind = ZoneRes[1]
         zonecurrenttemp = ZoneRes[3]
         zonestate = ZoneRes[2]
     else:
       statusRes = get_preset_zone(statuszone)
       if zonefound == True:
         zoneID = statusRes[0]
         zonename = statusRes[1]  
         zonetype = statusRes[6]
         zoneactiveind = statusRes[2]
         zonecurrenttemp = statusRes[7]
         zonestate = statusRes[3]
     
     if zonefound == True:
       write_log ('Alexa status request ok', statuszone)
       status_msg = 'The ' + str(zonename) + ' zone '
       if zonestate == "ON":
         Override_get = db.cursor()
         try:
           Override_get.execute("SELECT Override_Temp, Override_end FROM override_b WHERE Override_end > NOW() and Zone_ID = %s", (zoneID))
         except MySQLdb.Error as err:
           write_log ('Alexa SQL#48', '*** ERROR *** Selecting from Override')
           Error_state = True
           status_msg = 'Something went wrong, please report error #48'

         if not Error_state:  
           numrows = int (Override_get.rowcount)
           if numrows == 0:
		     if zonetype == "T": 
               status_msg = status_msg + ' is currently on due to a schedule and is at ' + str(zonecurrenttemp) + ' degrees'
             else:			 
			   status_msg = status_msg + ' is currently on due to a schedule'
           else:

             if numrows == 1:
               overrideRes = Override_get.fetchone()
               override_temp = overrideRes[0]
               override_end = overrideRes[1]
               nowt = datetime.datetime.now()
               
               tfmt = '%Y-%m-%d %H:%M:%S'
               
               tnow = time.mktime(nowt.timetuple())
               tend = time.mktime(override_end.timetuple())
               boostleft = int(tend-tnow) / 60
               
               if zonetype == "T":
                 status_msg = status_msg + 'is currently at ' +str(zonecurrenttemp) + ' degrees and has an active boost at ' + str(round(override_temp,1)) + ' degrees and will run for another ' + str(boostleft)+ ' minutes'
               else:
                 status_msg = status_msg + 'has an active boost and will run for another ' + str(boostleft)+ ' minutes'
             else:
               status_msg = status_msg + ' is currently on due to a boost but i found a multiple active boosts, thats kinda weird'
         Override_get.close()
         db.commit()
       else:
         if zoneactiveind == "N":
           status_msg = status_msg + ' but is currently disabled'
         else:
           if zonetype == "T":
             status_msg = status_msg + ' is at ' + str(zonecurrenttemp) + ' degrees and is enabled but is not currently on'
           else:
             status_msg = status_msg + ' is enabled but is not currently on'
     else:
       status_msg = 'The zone requested was not found, please try again'
       write_log ('Alexa bad status request - not found', statuszone)

   return statement(status_msg)



############################################################################################################################################
############################################################   Help Message   ##############################################################
############################################################################################################################################
  
@ask.intent('AMAZON.HelpIntent')
def help():
   
#   msg = "you can boost a zone by saying ...  boost zone 1 for 10 minutes at 20 degrees ... you must specify the duration in minutes, so 2 hours would be 120 minutes.  To cancel a zone just say the word cancel then the zone number "
#   msg = msg + "....you can also request the current temperature of a zone by asking how warm is it in zone 3 for example"
#   msg = msg + "....you can also boost the hotwater using the presets by simply saying...hotwater"
    msg = "Seriously?  You need lots of help, but not the sort i can offer."
    write_log ('Alexa request', 'Some dumbass requested help')
    return statement(msg)

@ask.intent("AMAZON.FallbackIntent")
def fallback():
   
#   msg = "you can boost a zone by saying ...  boost zone 1 for 10 minutes at 20 degrees ... you must specify the duration in minutes, so 2 hours would be 120 minutes.  To cancel a zone just say the word cancel then the zone number "
#   msg = msg + "....you can also request the current temperature of a zone by asking how warm is it in zone 3 for example"
#   msg = msg + "....you can also boost the hotwater using the presets by simply saying...hotwater"
    msg = "That command does not  match anything total control expects, you're wasting my time punk"
    write_log ('Alexa request', 'Ended up in fallback')
    return statement(msg)




if __name__ == '__main__':
    app.run(debug=True)
