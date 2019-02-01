if pgrep -f "python protosen.py" > /dev/null
then
    echo "protosen.py process is running"
#   nohup sudo python /home/pi/led/logger.py "Process check run" "Protosen.py found running ok" &
    exit
else
    sudo python /home/pi/led/alerter.py "Alerter  - Protosen Error" "Process protosen.py was not found, attempting restart.  Support are notified."
    cd /
    cd home/pi/led
    nohup sudo python protosen.py > /home/pi/logs/protosen.log 2>&1 &
    cd /
fi
