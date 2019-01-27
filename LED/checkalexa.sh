#!/bin/bash
# This job checks if alexa is turned on, if it is, it checks the python job is running
# if the job then isn't running, it emails

pwfile=$(cat /home/pi/led/pwsf.txt)
part=${pwfile:4:6}

start="TC"
end="9000"
password="$start$part$end"
myvar=$(mysql -u TCROOT9000 -p$password BoilerControl -NBse "SELECT * FROM params_b WHERE Param_Name = 'Alexa_YN'")
Alexa_YN="$(echo $myvar | cut -d' ' -f2 )"

if [ "$Alexa_YN" == "Y" ]
then
   if pgrep -f "python TCAlexa.py" > /dev/null
   then
      echo "TCAlexa.py process is running"
   else
      echo "TCAlexa.py process is not running - ohhh no"
      sudo python /home/pi/led/alerter.py "Alerter  - TCAlexa Error" "Process TCAlexa.py was not found but param is on check logs and restart"
   fi
fi
