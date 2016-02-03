if pgrep -f "python protosenUDP.py" > /dev/null
then
    echo "protosenUDP.py process is running"
#   nohup sudo python /home/pi/led/logger.py "Process check run" "Protosen.py found running ok" &
    exit
else
    sudo python /home/pi/led/alerter.py "TC9000 Alert  - Protosen Error" "Process protosenUDP.py was not found, check logs and restart"
fi
