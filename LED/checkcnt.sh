if pgrep -f "python control1.py" > /dev/null
then
    echo "Control1.py process is running"
#    nohup sudo python /home/pi/led/logger.py "Process check run" "Control1.py found running ok" &
    exit
else
    echo "Control1.py process is not running - ohhh no"
    sudo python /home/pi/led/alerter.py "Alerter  - Control1 Error" "Process Control1.py was not found, check logs and restart"
fi
