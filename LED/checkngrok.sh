#!/bin/bash
# This job checks if alexa is turned on, if it is, it checks the current ngrok address and 
# if its changed it alerts the user and updates the param table

pwfile=$(cat /home/pi/led/pwsf.txt)
part=${pwfile:4:6}

start="TC"
end="9000"
password="$start$part$end"
myvar=$(mysql -u TCROOT9000 -p$password BoilerControl -NBse "SELECT * FROM params_b WHERE Param_Name = 'Alexa_YN'")
Alexa_YN="$(echo $myvar | cut -d' ' -f2 )"

if [ "$Alexa_YN" == "Y" ]
then
    cd /
    cd home/pi/led
    sleep 2
    nohup sudo python checkngrok.py &
    cd /  
fi
